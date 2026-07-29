from typing import TypedDict, List, Dict, Any, Optional
import json
from langgraph.graph import StateGraph, END
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
from app.core.config import settings
from app.infrastructure.persistence.neo4j.repositories.neo4j_graph_repository import Neo4jGraphRepository
from neo4j import AsyncSession


class PRRiskState(TypedDict):
    # Inputs
    pr_id: str
    repo_name: str
    pr_title: str
    author_email: str
    additions: int
    deletions: int
    changed_files: int
    commit_shas: List[str]
    neo4j_session: Optional[Any]

    # Graph Context Enrichment
    neo4j_blast_radius: Dict[str, Any]
    developer_history: Dict[str, Any]

    # Agent Outputs
    risk_score: float
    risk_level: str
    reasoning: List[str]
    evidence: List[Dict[str, Any]]
    suggested_reviewers: List[str]


async def node_fetch_blast_radius(state: PRRiskState) -> Dict[str, Any]:
    """
    Node 1: Queries Neo4j Knowledge Graph for architectural blast radius
    """
    session: Optional[AsyncSession] = state.get("neo4j_session")
    if session:
        graph_repo = Neo4jGraphRepository(session)
        blast_radius = await graph_repo.get_pr_blast_radius(state["pr_id"])
    else:
        # Fallback heuristic if Neo4j session is detached
        blast_radius = {
            "touched_services": [state["repo_name"]],
            "databases_at_risk": [],
            "dependent_downstream_services": [],
            "historical_incidents": []
        }

    return {"neo4j_blast_radius": blast_radius}


async def node_fetch_developer_history(state: PRRiskState) -> Dict[str, Any]:
    """
    Node 2: Evaluates developer historical tenure & change failure metrics
    """
    # Simulated historical metrics computation
    history = {
        "author_email": state["author_email"],
        "total_prs_merged": 48,
        "historical_change_failure_rate": 0.02, # 2% CFR
        "domain_experience_level": "Senior Lead",
        "previous_incidents_caused": 0
    }
    return {"developer_history": history}


async def node_llm_risk_reasoning(state: PRRiskState) -> Dict[str, Any]:
    """
    Node 3: LangGraph OpenAI LLM Synthesizer for Risk Score, Reasoning & Reviewers
    """
    blast_radius = state["neo4j_blast_radius"]
    dev_history = state["developer_history"]

    prompt = f"""
You are the Principal AI SRE Risk Assessor for EngineeringOS AI.
Analyze the following Pull Request details, Neo4j Knowledge Graph blast radius, and Developer History to compute risk score, reasoning, evidence, and suggested code reviewers.

--- PR METRICS ---
PR ID: {state['pr_id']}
Title: {state['pr_title']}
Repository: {state['repo_name']}
Additions: {state['additions']} | Deletions: {state['deletions']} | Changed Files: {state['changed_files']}
Commits: {len(state['commit_shas'])}

--- NEO4J KNOWLEDGE GRAPH BLAST RADIUS ---
Touched Microservices: {blast_radius.get('touched_services', [])}
Databases at Risk: {blast_radius.get('databases_at_risk', [])}
Downstream Dependent Services: {blast_radius.get('dependent_downstream_services', [])}
Historical Incidents on Touched Services: {blast_radius.get('historical_incidents', [])}

--- DEVELOPER HISTORY ---
Author Email: {dev_history['author_email']}
Historical Change Failure Rate: {dev_history['historical_change_failure_rate'] * 100}%
Total Merged PRs: {dev_history['total_prs_merged']}

Respond ONLY in valid JSON with the following key structure:
{{
  "risk_score": <float 0.0 to 100.0>,
  "risk_level": "<LOW | MEDIUM | HIGH | CRITICAL>",
  "reasoning": ["<bullet 1>", "<bullet 2>", ...],
  "evidence": [
    {{"category": "<category>", "detail": "<detail>"}}
  ],
  "suggested_reviewers": ["<expert_email_1>", "<expert_email_2>"]
}}
"""

    try:
        llm = ChatOpenAI(
            model=settings.OPENAI_MODEL,
            openai_api_key=settings.OPENAI_API_KEY,
            temperature=0.1
        )
        response = await llm.ainvoke([
            SystemMessage(content="You produce structured JSON output for enterprise AI software engineering risk assessment."),
            HumanMessage(content=prompt)
        ])
        content = response.content.strip()
        # Handle code block markdown if present
        if content.startswith("```json"):
            content = content.split("```json")[1].split("```")[0].strip()
        result = json.loads(content)
    except Exception as e:
        # Robust Deterministic Fallback Evaluator if OpenAI API is offline
        code_churn = state["additions"] + state["deletions"]
        base_score = min(90.0, (code_churn / 20.0) + (len(blast_radius.get("databases_at_risk", [])) * 25.0))
        level = "LOW" if base_score < 30 else ("MEDIUM" if base_score < 60 else "HIGH")
        
        result = {
            "risk_score": round(base_score, 1),
            "risk_level": level,
            "reasoning": [
                f"Calculated code churn of {code_churn} lines across {state['changed_files']} files.",
                f"Touched {len(blast_radius.get('touched_services', []))} microservices in Neo4j Knowledge Graph."
            ],
            "evidence": [
                {"category": "Code Churn", "detail": f"{state['additions']} additions, {state['deletions']} deletions"},
                {"category": "Knowledge Graph", "detail": f"Services touched: {blast_radius.get('touched_services', [])}"}
            ],
            "suggested_reviewers": ["sre-lead@company.com", "architecture-owner@company.com"]
        }

    return {
        "risk_score": result["risk_score"],
        "risk_level": result["risk_level"],
        "reasoning": result["reasoning"],
        "evidence": result["evidence"],
        "suggested_reviewers": result["suggested_reviewers"]
    }


def build_pr_risk_agent():
    """
    Constructs and compiles the LangGraph StateGraph agent for PR Risk Assessment.
    """
    workflow = StateGraph(PRRiskState)

    workflow.add_node("fetch_blast_radius", node_fetch_blast_radius)
    workflow.add_node("fetch_developer_history", node_fetch_developer_history)
    workflow.add_node("llm_risk_reasoning", node_llm_risk_reasoning)

    workflow.set_entry_point("fetch_blast_radius")
    workflow.add_edge("fetch_blast_radius", "fetch_developer_history")
    workflow.add_edge("fetch_developer_history", "llm_risk_reasoning")
    workflow.add_edge("llm_risk_reasoning", END)

    return workflow.compile()
