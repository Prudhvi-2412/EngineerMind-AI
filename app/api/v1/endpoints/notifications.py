from fastapi import APIRouter, Depends, status
from app.api.schemas.notification_schemas import (
    SendAlertNotificationRequest,
    SendAlertNotificationResponse,
    DispatchReportResponse,
)
from app.application.notifications.alert_engine import AlertEngine
from app.application.notifications.report_generator import ReportGeneratorService
from app.api.dependencies.auth_deps import get_current_user
from app.domain.entities.user import User

router = APIRouter(prefix="/notifications", tags=["Multi-Channel Notification Service & Alert Engine"])


@router.post("/send", response_model=SendAlertNotificationResponse, status_code=status.HTTP_200_OK)
async def send_risk_alert_notification(
    payload: SendAlertNotificationRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Dispatches operational risk alert concurrently across Slack, Email, GitHub PR Comments, and Microsoft Teams.
    """
    engine = AlertEngine()
    results = await engine.dispatch_risk_alert(
        title=payload.title,
        message=payload.message,
        severity=payload.severity,
        metadata=payload.metadata
    )

    return SendAlertNotificationResponse(
        title=payload.title,
        severity=payload.severity,
        channel_dispatch_results=results
    )


@router.post("/reports/daily", response_model=DispatchReportResponse, status_code=status.HTTP_200_OK)
async def dispatch_daily_digest_report(
    current_user: User = Depends(get_current_user)
):
    """
    Generates and dispatches the Daily Engineering Telemetry Digest report.
    """
    generator = ReportGeneratorService()
    res = await generator.generate_and_dispatch_daily_report()
    return DispatchReportResponse(
        report_title=res["report_title"],
        dispatch_results=res["dispatch_results"]
    )


@router.post("/reports/weekly", response_model=DispatchReportResponse, status_code=status.HTTP_200_OK)
async def dispatch_weekly_digest_report(
    current_user: User = Depends(get_current_user)
):
    """
    Generates and dispatches the Weekly Executive Engineering Digest report.
    """
    generator = ReportGeneratorService()
    res = await generator.generate_and_dispatch_weekly_report()
    return DispatchReportResponse(
        report_title=res["report_title"],
        dispatch_results=res["dispatch_results"]
    )
