from fastapi import APIRouter, Depends, status
from neo4j import AsyncSession
from app.api.schemas.agent_schemas import AnalyzePRRiskRequest, PRRiskResponse
from app.application.agents.pr_risk_agent import build_pr_risk_agent
from app.infrastructure.persistence.neo4j.connection import get_neo4j_session
from app.api.dependencies.auth_deps import get_current_user
from app.domain.entities.user import User

router = APIRouter(prefix="/agents", tags=["LangGraph AI Agents & Engineering Risk Intelligence"])


@router.post("/pr-risk/analyze", response_model=PRRiskResponse, status_code=status.HTTP_200_OK)
async def analyze_pr_risk(
    payload: AnalyzePRRiskRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_neo4j_session)
):
    """
    Execute LangGraph PR Risk Assessment AI Agent.
    Synthesizes Neo4j Knowledge Graph blast radius, developer history, and code churn into risk score, reasoning, evidence, and suggested reviewers.
    """
    agent = build_pr_risk_agent()

    initial_state = {
        "pr_id": payload.pr_id,
        "repo_name": payload.repo_name,
        "pr_title": payload.pr_title,
        "author_email": payload.author_email,
        "additions": payload.additions,
        "deletions": payload.deletions,
        "changed_files": payload.changed_files,
        "commit_shas": payload.commit_shas,
        "neo4j_session": session,
        "neo4j_blast_radius": {},
        "developer_history": {},
        "risk_score": 0.0,
        "risk_level": "LOW",
        "reasoning": [],
        "evidence": [],
        "suggested_reviewers": []
    }

    final_state = await agent.ainvoke(initial_state)

    return PRRiskResponse(
        pr_id=payload.pr_id,
        risk_score=final_state["risk_score"],
        risk_level=final_state["risk_level"],
        reasoning=final_state["reasoning"],
        evidence=final_state["evidence"],
        suggested_reviewers=final_state["suggested_reviewers"]
    )


@router.post("/architecture-review/analyze", response_model=ArchitectureReviewResponse, status_code=status.HTTP_200_OK)
async def analyze_architecture(
    payload: AnalyzeArchitectureRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_neo4j_session)
):
    """
    Execute LangGraph Architecture Review AI Agent.
    Evaluates microservice coupling, circular dependencies, God Classes, SOLID principles, and Clean Architecture adherence.
    """
    from app.application.agents.architecture_review_agent import build_architecture_review_agent

    agent = build_architecture_review_agent()

    initial_state = {
        "repo_name": payload.repo_name,
        "file_tree": payload.file_tree,
        "dependencies": payload.dependencies,
        "code_snippets": payload.code_snippets,
        "neo4j_session": session,
        "coupling_analysis": {},
        "circular_dependencies": [],
        "god_classes": [],
        "solid_violations": [],
        "clean_arch_compliance_score": 100.0,
        "tech_debt_score": 0.0,
        "architecture_report": "",
        "recommendations": []
    }

    final_state = await agent.ainvoke(initial_state)

    return ArchitectureReviewResponse(
        repo_name=payload.repo_name,
        tech_debt_score=final_state["tech_debt_score"],
        clean_arch_compliance_score=final_state["clean_arch_compliance_score"],
        circular_dependencies_count=len(final_state["circular_dependencies"]),
        god_classes_count=len(final_state["god_classes"]),
        architecture_report=final_state["architecture_report"],
        recommendations=final_state["recommendations"]
    )


@router.post("/sprint-prediction/analyze", response_model=SprintPredictionResponse, status_code=status.HTTP_200_OK)
async def analyze_sprint_prediction(
    payload: AnalyzeSprintPredictionRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Execute LangGraph Sprint Prediction AI Agent.
    Synthesizes Jira burndown trajectory, story points completed, velocity deficit ratio, and blocked tasks to predict Sprint Success % & Delay Probability %.
    """
    from app.application.agents.sprint_prediction_agent import build_sprint_prediction_agent

    agent = build_sprint_prediction_agent()

    initial_state = {
        "sprint_id": payload.sprint_id,
        "sprint_name": payload.sprint_name,
        "total_story_points": payload.total_story_points,
        "completed_story_points": payload.completed_story_points,
        "days_remaining": payload.days_remaining,
        "historical_team_velocity": payload.historical_team_velocity,
        "blocked_tasks_count": payload.blocked_tasks_count,
        "blocked_tasks_details": payload.blocked_tasks_details,
        "remaining_story_points": 0.0,
        "required_daily_velocity": 0.0,
        "burndown_trend_slope": 0.0,
        "velocity_deficit_ratio": 1.0,
        "sprint_success_percentage": 0.0,
        "delay_probability": 0.0,
        "reasons": [],
        "recommendations": []
    }

    final_state = await agent.ainvoke(initial_state)

    return SprintPredictionResponse(
        sprint_id=payload.sprint_id,
        sprint_name=payload.sprint_name,
        sprint_success_percentage=final_state["sprint_success_percentage"],
        delay_probability=final_state["delay_probability"],
        reasons=final_state["reasons"],
        recommendations=final_state["recommendations"]
    )


@router.post("/incident-prediction/predict", response_model=IncidentPredictionResponse, status_code=status.HTTP_200_OK)
async def predict_incident(
    payload: PredictIncidentRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_neo4j_session)
):
    """
    Execute LangGraph Incident Prediction & Root Cause AI Agent.
    Correlates Prometheus metrics, Grafana alerts, log anomalies, Kubernetes deployments, and Neo4j dependency blast radius to predict incidents and suggest SRE mitigations.
    """
    from app.application.agents.incident_prediction_agent import build_incident_prediction_agent

    agent = build_incident_prediction_agent()

    initial_state = {
        "service_name": payload.service_name,
        "time_window_minutes": payload.time_window_minutes,
        "prometheus_metrics": payload.prometheus_metrics,
        "grafana_alerts": payload.grafana_alerts,
        "log_anomalies": payload.log_anomalies,
        "recent_deployments": payload.recent_deployments,
        "neo4j_session": session,
        "telemetry_severity_score": 0.0,
        "dependency_graph_context": {},
        "predicted_incident_risk": 0.0,
        "predicted_incident_level": "NONE",
        "root_cause_analysis": "",
        "affected_services": [],
        "mitigation_steps": []
    }

    final_state = await agent.ainvoke(initial_state)

    return IncidentPredictionResponse(
        service_name=payload.service_name,
        predicted_incident_risk=final_state["predicted_incident_risk"],
        predicted_incident_level=final_state["predicted_incident_level"],
        root_cause_analysis=final_state["root_cause_analysis"],
        affected_services=final_state["affected_services"],
        mitigation_steps=final_state["mitigation_steps"]
    )


@router.post("/developer-insights/analyze", response_model=DeveloperInsightResponse, status_code=status.HTTP_200_OK)
async def analyze_developer_insights(
    payload: AnalyzeDeveloperInsightRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_neo4j_session)
):
    """
    Execute LangGraph Developer Insight & Burnout AI Agent.
    Evaluates developer code ownership %, bus factor knowledge distribution, review quality, weekly workload hours, late night commits, and burnout risk indicators.
    """
    from app.application.agents.developer_insight_agent import build_developer_insight_agent

    agent = build_developer_insight_agent()

    initial_state = {
        "developer_email": payload.developer_email,
        "time_window_days": payload.time_window_days,
        "neo4j_session": session,
        "code_ownership_matrix": {},
        "domain_expertise_tags": [],
        "knowledge_distribution_score": 0.0,
        "review_quality_score": 0.0,
        "weekly_workload_hours": 0.0,
        "late_night_commit_count": 0,
        "weekend_commit_count": 0,
        "burnout_risk_score": 0.0,
        "burnout_risk_level": "LOW",
        "burnout_indicators": [],
        "insights_summary": "",
        "recommendations": []
    }

    final_state = await agent.ainvoke(initial_state)

    return DeveloperInsightResponse(
        developer_email=payload.developer_email,
        code_ownership_matrix=final_state["code_ownership_matrix"],
        domain_expertise_tags=final_state["domain_expertise_tags"],
        knowledge_distribution_score=final_state["knowledge_distribution_score"],
        review_quality_score=final_state["review_quality_score"],
        weekly_workload_hours=final_state["weekly_workload_hours"],
        burnout_risk_score=final_state["burnout_risk_score"],
        burnout_risk_level=final_state["burnout_risk_level"],
        burnout_indicators=final_state["burnout_indicators"],
        insights_summary=final_state["insights_summary"],
        recommendations=final_state["recommendations"]
    )




