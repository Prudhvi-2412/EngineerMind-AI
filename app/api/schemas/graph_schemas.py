from typing import List, Optional
from pydantic import BaseModel, Field


class SyncPRGraphRequest(BaseModel):
    pr_id: str = Field(..., example="PR-1042")
    title: str = Field(..., example="Upgrade Payment Gateway API client")
    author_email: str = Field(..., example="developer@company.com")
    author_name: str = Field(..., example="John Developer")
    repo_full_name: str = Field(..., example="acme/payment-service")
    touched_services: List[str] = Field(..., example=["payment-service", "billing-service"])


class BlastRadiusResponse(BaseModel):
    pr_id: str
    title: Optional[str] = None
    author_email: Optional[str] = None
    touched_services: List[str] = []
    databases_at_risk: List[str] = []
    dependent_downstream_services: List[str] = []
    historical_incidents: List[str] = []


class RootCauseResponse(BaseModel):
    incident_id: Optional[str] = None
    incident_title: Optional[str] = None
    deployment_id: Optional[str] = None
    pr_id: Optional[str] = None
    pr_title: Optional[str] = None
    author_name: Optional[str] = None
    author_email: Optional[str] = None
    affected_service: Optional[str] = None
