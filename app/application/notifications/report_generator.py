from typing import Dict, Any
from app.application.notifications.alert_engine import AlertEngine


class ReportGeneratorService:
    """
    Generates structured Daily Digest and Weekly Executive Reports for automated notification dispatch.
    """

    def __init__(self, alert_engine: AlertEngine = None):
        self.alert_engine = alert_engine or AlertEngine()

    async def generate_and_dispatch_daily_report(self, org_slug: str = "Acme-Corp") -> Dict[str, Any]:
        report_title = f"📅 Daily Engineering Telemetry Digest — {org_slug}"
        report_markdown = """
### 🚀 Daily Engineering Telemetry Summary

- **Deployment Frequency:** 4.2 / day (Elite Status)
- **Active PR Blast Radius Warnings:** 1 High-Risk PR (`PR-2048`)
- **Open Prometheus Alerts:** 0 Firing
- **Sprint 42 Burndown:** On Track (62.5% Success Probability)

*Generated automatically by EngineeringOS AI.*
"""
        results = {}
        for provider in self.alert_engine.providers:
            res = await provider.send_report(report_title, report_markdown, "engineering-leads@company.com")
            results[provider.__class__.__name__] = res

        return {"report_title": report_title, "dispatch_results": results}

    async def generate_and_dispatch_weekly_report(self, org_slug: str = "Acme-Corp") -> Dict[str, Any]:
        report_title = f"📊 Weekly Executive Engineering Digest — {org_slug}"
        report_markdown = """
### 🏢 Executive Weekly Engineering Digest

- **Overall Engineering Health Score:** `88.5 / 100`
- **Weekly Lead Time for Changes:** `1.8 hours`
- **Team Burnout Risk Rating:** `LOW` (Avg Workload: 42.5 hrs/wk)
- **Estimated Cloud Infrastructure Spend:** `$14,250` (-4.5% change)
- **Top Weekly Contributor:** Alex Rivera (48 commits, 12 PRs)

*Generated automatically by EngineeringOS AI Engine.*
"""
        results = {}
        for provider in self.alert_engine.providers:
            res = await provider.send_report(report_title, report_markdown, "executive-team@company.com")
            results[provider.__class__.__name__] = res

        return {"report_title": report_title, "dispatch_results": results}
