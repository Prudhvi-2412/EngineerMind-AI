from typing import List, Dict, Any
from pydantic import BaseModel, Field


class AnalyzePRRiskRequest(BaseModel):
    pr_id: str = Field(..., example="PR-2048")
    repo_name: str = Field(..., example="acme/payment-gateway")
    pr_title: str = Field(..., example="Refactor payment processor and schema migration")
    author_email: str = Field(..., example="dev@company.com")
    additions: int = Field(150, example=240)
    deletions: int = Field(30, example=45)
    changed_files: int = Field(5, example=8)
    commit_shas: List[str] = Field(default_factory=list, example=["a1b2c3d", "e5f6g7h"])


class PRRiskResponse(BaseModel):
    pr_id: str
    risk_score: float
    risk_level: str
    reasoning: List[str]
    evidence: List[Dict[str, Any]]
    suggested_reviewers: List[str]


class AnalyzeArchitectureRequest(BaseModel):
    repo_name: str = Field(..., example="acme/billing-microservice")
    file_tree: List[str] = Field(default_factory=list, example=["src/main.py", "src/services/billing.py"])
    dependencies: Dict[str, str] = Field(default_factory=dict, example={"fastapi": "0.110.0", "sqlalchemy": "2.0.28"})
    code_snippets: Dict[str, str] = Field(default_factory=dict, example={"src/services/billing.py": "class BillingMonolith: pass"})


class ArchitectureReviewResponse(BaseModel):
    repo_name: str
    tech_debt_score: float
    clean_arch_compliance_score: float
    circular_dependencies_count: int
    god_classes_count: int
    architecture_report: str
    recommendations: List[str]


class AnalyzeSprintPredictionRequest(BaseModel):
    sprint_id: str = Field(..., example="SPRINT-42")
    sprint_name: str = Field(..., example="Sprint 42 - Q3 Payment Engine")
    total_story_points: float = Field(..., example=80.0)
    completed_story_points: float = Field(..., example=32.0)
    days_remaining: int = Field(..., example=4)
    historical_team_velocity: float = Field(..., example=45.0)
    blocked_tasks_count: int = Field(..., example=2)
    blocked_tasks_details: List[Dict[str, Any]] = Field(default_factory=list, example=[{"key": "ENG-104", "story_points": 5}])


class SprintPredictionResponse(BaseModel):
    sprint_id: str
    sprint_name: str
    sprint_success_percentage: float
    delay_probability: float
    reasons: List[str]
    recommendations: List[str]


class PredictIncidentRequest(BaseModel):
    service_name: str = Field(..., example="auth-service")
    time_window_minutes: int = Field(30, example=30)
    prometheus_metrics: Dict[str, Any] = Field(
        default_factory=dict,
        example={"cpu_utilization_percent": 88.5, "memory_utilization_percent": 92.0, "p99_latency_ms": 650.0, "error_rate_percent": 4.5}
    )
    grafana_alerts: List[Dict[str, Any]] = Field(
        default_factory=list,
        example=[{"ruleName": "High HTTP 5xx Rate", "state": "alerting"}]
    )
    log_anomalies: List[str] = Field(
        default_factory=list,
        example=["java.lang.OutOfMemoryError: Java heap space", "Connection timed out to auth_db:5432"]
    )
    recent_deployments: List[Dict[str, Any]] = Field(
        default_factory=list,
        example=[{"deployment_id": "dep-904", "sha": "c0ffe33", "timestamp": "2026-07-29T11:00:00Z"}]
    )


class IncidentPredictionResponse(BaseModel):
    service_name: str
    predicted_incident_risk: float
    predicted_incident_level: str
    root_cause_analysis: str
    affected_services: List[str]
    mitigation_steps: List[str]


class AnalyzeDeveloperInsightRequest(BaseModel):
    developer_email: str = Field(..., example="engineer@company.com")
    time_window_days: int = Field(30, example=30)


class DeveloperInsightResponse(BaseModel):
    developer_email: str
    code_ownership_matrix: Dict[str, float]
    domain_expertise_tags: List[str]
    knowledge_distribution_score: float
    review_quality_score: float
    weekly_workload_hours: float
    burnout_risk_score: float
    burnout_risk_level: str
    burnout_indicators: List[str]
    insights_summary: str
    recommendations: List[str]




