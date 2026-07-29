import pytest
from app.application.agents.incident_prediction_agent import build_incident_prediction_agent


@pytest.mark.asyncio
async def test_incident_prediction_agent_execution():
    agent = build_incident_prediction_agent()

    initial_state = {
        "service_name": "payment-service",
        "time_window_minutes": 30,
        "prometheus_metrics": {
            "cpu_utilization_percent": 94.0,
            "memory_utilization_percent": 89.0,
            "p99_latency_ms": 780.0,
            "error_rate_percent": 6.2
        },
        "grafana_alerts": [{"ruleName": "High HTTP 5xx Rate", "state": "alerting"}],
        "log_anomalies": ["java.lang.OutOfMemoryError: Java heap space"],
        "recent_deployments": [{"deployment_id": "dep-904", "sha": "c0ffe33"}],
        "neo4j_session": None,
        "telemetry_severity_score": 0.0,
        "dependency_graph_context": {},
        "predicted_incident_risk": 0.0,
        "predicted_incident_level": "NONE",
        "root_cause_analysis": "",
        "affected_services": [],
        "mitigation_steps": []
    }

    final_state = await agent.ainvoke(initial_state)

    assert "predicted_incident_risk" in final_state
    assert isinstance(final_state["predicted_incident_risk"], float)
    assert final_state["predicted_incident_level"] in ("NONE", "LOW", "MEDIUM", "HIGH", "CRITICAL")
    assert len(final_state["root_cause_analysis"]) > 0
    assert len(final_state["affected_services"]) > 0
    assert len(final_state["mitigation_steps"]) > 0
