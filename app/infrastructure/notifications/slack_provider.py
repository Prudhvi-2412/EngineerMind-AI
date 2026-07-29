import httpx
from typing import Dict, Any, Optional
from tenacity import retry, stop_after_attempt, wait_exponential
from app.domain.interfaces.notification_provider import INotificationProvider


class SlackNotificationProvider(INotificationProvider):
    """
    Slack Multi-Channel Provider supporting Block Kit webhooks & bot messaging.
    """

    def __init__(self, webhook_url: Optional[str] = None):
        self.webhook_url = webhook_url or "https://hooks.slack.com/services/mock/webhook"

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    async def send_alert(self, title: str, message: str, severity: str, metadata: Optional[Dict[str, Any]] = None) -> bool:
        color = "#ef4444" if severity in ("HIGH", "CRITICAL") else ("#f59e0b" if severity == "MEDIUM" else "#10b981")
        
        payload = {
            "attachments": [
                {
                    "color": color,
                    "title": f"🚨 [EngineeringOS AI] {title}",
                    "text": message,
                    "fields": [
                        {"title": "Severity", "value": severity, "short": True},
                        {"title": "Source", "value": metadata.get("source", "Telemetry Engine") if metadata else "Engine", "short": True}
                    ],
                    "footer": "EngineeringOS Risk Alert Engine"
                }
            ]
        }
        
        async with httpx.AsyncClient() as client:
            resp = await client.post(self.webhook_url, json=payload, timeout=5.0)
            return resp.status_code < 400

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    async def send_report(self, report_title: str, report_markdown: str, recipient: str) -> bool:
        payload = {
            "text": f"📊 *{report_title}*\n\n{report_markdown}"
        }
        async with httpx.AsyncClient() as client:
            resp = await client.post(self.webhook_url, json=payload, timeout=5.0)
            return resp.status_code < 400
