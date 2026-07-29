from typing import List, Dict, Any
from pydantic import BaseModel, Field


class ContributorSummary(BaseModel):
    name: str
    email: str
    commits_count: int
    prs_merged: int
    impact_score: float


class EngineeringEventSummary(BaseModel):
    event_id: str
    source: str
    event_type: str
    timestamp: str
    summary: str


class EngineeringHealthResponse(BaseModel):
    engineering_score: float = Field(..., example=88.5, description="Overall Engineering Health Score (0-100)")
    deployment_success_rate: float = Field(..., example=97.8, description="Deployment Success Rate %")
    sprint_health_score: float = Field(..., example=84.2, description="Sprint Health Score %")
    incident_risk_score: float = Field(..., example=12.4, description="Incident Risk % (Lower is better)")
    technical_debt_score: float = Field(..., example=24.0, description="Technical Debt Score (0-100)")
    cloud_cost_monthly: float = Field(..., example=14250.0, description="Estimated Monthly Cloud Infrastructure Spend ($)")
    cloud_cost_change_percent: float = Field(..., example=-4.5, description="Monthly Cloud Cost Change %")
    top_contributors: List[ContributorSummary]
    recent_events: List[EngineeringEventSummary]
