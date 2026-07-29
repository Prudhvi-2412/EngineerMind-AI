import pytest
from app.application.notifications.alert_engine import AlertEngine
from app.application.notifications.report_generator import ReportGeneratorService


@pytest.mark.asyncio
async def test_alert_engine_dispatch():
    engine = AlertEngine()
    results = await engine.dispatch_risk_alert(
        title="High Blast Radius PR Merged",
        message="PR-2048 touches payment-service and payment_db.",
        severity="HIGH",
        metadata={"repo": "acme/auth-service", "pr_number": 2048}
    )

    assert "SlackNotificationProvider" in results
    assert "EmailNotificationProvider" in results
    assert "GitHubCommentNotificationProvider" in results
    assert "MSTeamsNotificationProvider" in results


@pytest.mark.asyncio
async def test_report_generator_daily_dispatch():
    generator = ReportGeneratorService()
    res = await generator.generate_and_dispatch_daily_report(org_slug="Acme-Corp")

    assert "Daily Engineering Telemetry Digest" in res["report_title"]
    assert len(res["dispatch_results"]) >= 4
