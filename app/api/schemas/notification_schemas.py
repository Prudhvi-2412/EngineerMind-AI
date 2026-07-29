from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class SendAlertNotificationRequest(BaseModel):
    title: str = Field(..., example="High Blast Radius PR Merged in auth-service")
    message: str = Field(..., example="PR-2048 touches payment-service and payment_db database.")
    severity: str = Field("HIGH", example="HIGH")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, example={"source": "GitHub Webhook", "repo": "acme/auth-service"})


class SendAlertNotificationResponse(BaseModel):
    title: str
    severity: str
    channel_dispatch_results: Dict[str, bool]


class DispatchReportResponse(BaseModel):
    report_title: str
    dispatch_results: Dict[str, bool]
