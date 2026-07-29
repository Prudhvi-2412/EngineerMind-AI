import httpx
from typing import Dict, Any, Optional
from tenacity import retry, stop_after_attempt, wait_exponential
from app.domain.interfaces.notification_provider import INotificationProvider


class MSTeamsNotificationProvider(INotificationProvider):
    """
    Microsoft Teams Adaptive Cards Notification Provider.
    """

    def __init__(self, webhook_url: Optional[str] = None):
        self.webhook_url = webhook_url or "https://outlook.office.com/webhook/mock"

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    async def send_alert(self, title: str, message: str, severity: str, metadata: Optional[Dict[str, Any]] = None) -> bool:
        card = {
            "@type": "MessageCard",
            "@context": "http://schema.org/extensions",
            "themeColor": "d97706" if severity == "MEDIUM" else ("dc2626" if severity in ("HIGH", "CRITICAL") else "16a34a"),
            "summary": title,
            "sections": [
                {
                    "activityTitle": f"⚠️ EngineeringOS AI: {title}",
                    "activitySubtitle": f"Severity: {severity}",
                    "text": message
                }
            ]
        }
        async with httpx.AsyncClient() as client:
            resp = await client.post(self.webhook_url, json=card, timeout=5.0)
            return resp.status_code < 400

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    async def send_report(self, report_title: str, report_markdown: str, recipient: str) -> bool:
        card = {
            "@type": "MessageCard",
            "summary": report_title,
            "sections": [{"activityTitle": report_title, "text": report_markdown}]
        }
        async with httpx.AsyncClient() as client:
            resp = await client.post(self.webhook_url, json=card, timeout=5.0)
            return resp.status_code < 400
