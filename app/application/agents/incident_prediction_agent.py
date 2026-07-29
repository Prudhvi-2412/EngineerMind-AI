from typing import TypedDict, List, Dict, Any, Optional
import json
from langgraph.graph import StateGraph, END
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
from app.core.config import settings
from app.infrastructure.persistence.neo4j.repositories.neo4j_graph_repository import Neo4jGraphRepository
from neo4j import AsyncSession


class IncidentPredictionState(TypedDict):
    # Inputs
    service_name: str
    time_window_minutes: int
    prometheus_metrics: Dict[str, Any]
    grafana_alerts: List[Dict[str, Any]]
    log_anomalies: List[str]
    recent_deployments: List[Dict[str, Any]]
    neo4j_session: Optional[Any]

    # Intermediate Context
    telemetry_severity_score: float
    dependency_graph_context: Dict[str, Any]

    # Agent Outputs
    predicted_incident_risk: float
    predicted_incident_level: str
    root_cause_analysis: str
    affected_services: List[str]
    mitigation_steps: List[str]


async def node_aggregate_telemetry_and_logs(state: IncidentPredictionState) -> Dict[str, Any]:
    """
    Node 1: Evaluates Prometheus metrics, log anomaly counts, and deployment events
    """
    prom = state.get("prometheus_metrics", {})
    cpu = prom.get("cpu_utilization_percent", 45.0)
    memory = prom.get("memory_utilization_percent", 50.0)
    p99_latency_ms = prom.get("p99_latency_ms", 120.0)
    error_rate_percent = prom.get("error_rate_percent", 0.1)

    log_anomalies_count = len(state.get("log_anomalies", []))
    grafana_alerts_count = len(state.get("grafana_alerts", []))
    deployments_count = len(state.get("recent_deployments", []))

    # Calculate telemetry severity heuristic
    severity = (
        (cpu / 100.0 * 20.0) +
        (memory / 100.0 * 20.0) +
        min(30.0, error_rate_percent * 10.0) +
        min(20.0, (p99_latency_ms / 500.0) * 20.0) +
        (log_anomalies_count * 5.0) +
        (grafana_alerts_count * 10.0)
    )

    return {"telemetry_severity_score": round(severity, 1)}


async def node_query_dependency_blast_radius(state: IncidentPredictionState) -> Dict[str, Any]:
    """
    Node 2: Traverses Neo4j Knowledge Graph for downstream dependent microservices and databases
    """
    session: Optional[AsyncSession] = state.get("neo4j_session")
    service_name = state["service_name"]

    affected = [service_name]
    graph_context = {
        "downstream_services": [],
        "databases": []
    }

    if session:
        cypher = """
        MATCH (s:Microservice {name: $service_name})
        OPTIONAL MATCH (other:Microservice)-[:DEPENDS_ON]->(s)
        OPTIONAL MATCH (s)-[:USES]->(db:Database)
        RETURN collect(DISTINCT other.name) as downstream, collect(DISTINCT db.name) as databases
        """
        try:
            res = await session.run(cypher, service_name=service_name)
            record = await res.single()
            if record:
                downstream = record["downstream"]
                databases = record["databases"]
                graph_context = {
                    "downstream_services": downstream,
                    "databases": databases
                }
                affected.extend(downstream)
        except Exception:
            pass

    return {
        "dependency_graph_context": graph_context,
        "affected_services": list(set(affected))
    }


async def node_llm_predict_incident_and_root_cause(state: IncidentPredictionState) -> Dict[str, Any]:
    """
    Node 3: OpenAI LLM Incident Predictor & Root Cause AI Specialist
    """
    prom = state["prometheus_metrics"]
    alerts = state["grafana_alerts"]
    logs = state["log_anomalies"]
    deployments = state["recent_deployments"]
    graph = state["dependency_graph_context"]
    service = state["service_name"]

    prompt = f"""
You are the Lead SRE AI Specialist for EngineeringOS AI.
Analyze the following multi-source telemetry, log anomalies, Kubernetes deployment events, and Neo4j dependency graphs to predict future operational incident risk, identify root cause, list affected services, and provide mitigation steps.

--- TARGET SERVICE ---
Service Name: {service}
Time Window: Last {state['time_window_minutes']} minutes

--- PROMETHEUS METRICS ---
CPU Utilization: {prom.get('cpu_utilization_percent', 'N/A')}%
Memory Utilization: {prom.get('memory_utilization_percent', 'N/A')}%
P99 Response Latency: {prom.get('p99_latency_ms', 'N/A')} ms
Http Error Rate: {prom.get('error_rate_percent', 'N/A')}%

--- GRAFANA ALERTS ({len(alerts)}) ---
{json.dumps(alerts, indent=2)}

--- LOG ANOMALIES ({len(logs)}) ---
{json.dumps(logs, indent=2)}

--- RECENT KUBERNETES DEPLOYMENTS ({len(deployments)}) ---
{json.dumps(deployments, indent=2)}

--- NEO4J DEPENDENCY GRAPH CONTEXT ---
Downstream Dependent Microservices: {graph.get('downstream_services', [])}
Databases at Risk: {graph.get('databases', [])}

Generate a JSON response with:
1. "predicted_incident_risk": Float (0.0 to 100.0).
2. "predicted_incident_level": String ("NONE" | "LOW" | "MEDIUM" | "HIGH" | "CRITICAL").
3. "root_cause_analysis": Comprehensive explanation of telemetry anomalies and deployment triggers.
4. "affected_services": Array of service names at risk of cascading failure.
5. "mitigation_steps": Array of actionable SRE remediation steps.

Respond ONLY in valid JSON:
{{
  "predicted_incident_risk": <float>,
  "predicted_incident_level": "<level>",
  "root_cause_analysis": "<analysis_string>",
  "affected_services": ["<service1>", "<service2>"],
  "mitigation_steps": ["<step1>", "<step2>"]
}}
"""

    try:
        llm = ChatOpenAI(
            model=settings.OPENAI_MODEL,
            openai_api_key=settings.OPENAI_API_KEY,
            temperature=0.1
        )
        response = await llm.ainvoke([
            SystemMessage(content="You produce structured JSON incident risk predictions and root cause analysis."),
            HumanMessage(content=prompt)
        ])
        content = response.content.strip()
        if content.startswith("```json"):
            content = content.split("```json")[1].split("```")[0].strip()
        result = json.loads(content)
    except Exception as e:
        # Fallback Evaluator if OpenAI API is offline
        risk = min(98.0, state["telemetry_severity_score"])
        level = "NONE" if risk < 20 else ("LOW" if risk < 45 else ("MEDIUM" if risk < 70 else "HIGH"))

        result = {
            "predicted_incident_risk": round(risk, 1),
            "predicted_incident_level": level,
            "root_cause_analysis": f"Elevated telemetry severity score ({state['telemetry_severity_score']}) triggered by recent deployment and log anomaly spikes on {service}.",
            "affected_services": state["affected_services"],
            "mitigation_steps": [
                f"Roll back recent deployment on microservice '{service}' to previous stable image.",
                "Scale up HPA replica count to absorb traffic latency spikes.",
                "Inspect DB connection pool metrics to prevent thread starvation."
            ]
        }

    return {
        "predicted_incident_risk": result["predicted_incident_risk"],
        "predicted_incident_level": result["predicted_incident_level"],
        "root_cause_analysis": result["root_cause_analysis"],
        "affected_services": result["affected_services"],
        "mitigation_steps": result["mitigation_steps"]
    }


def build_incident_prediction_agent():
    """
    Constructs and compiles the LangGraph StateGraph agent for Incident Prediction.
    """
    workflow = StateGraph(IncidentPredictionState)

    workflow.add_node("aggregate_telemetry_and_logs", node_aggregate_telemetry_and_logs)
    workflow.add_node("query_dependency_blast_radius", node_query_dependency_blast_radius)
    workflow.add_node("llm_predict_incident_and_root_cause", node_llm_predict_incident_and_root_cause)

    workflow.set_entry_point("aggregate_telemetry_and_logs")
    workflow.add_edge("aggregate_telemetry_and_logs", "query_dependency_blast_radius")
    workflow.add_edge("query_dependency_blast_radius", "llm_predict_incident_and_root_cause")
    workflow.add_edge("llm_predict_incident_and_root_cause", END)

    return workflow.compile()
