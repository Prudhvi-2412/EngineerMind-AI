from typing import Dict, Any, Optional
from tenacity import retry, stop_after_attempt, wait_exponential
from app.domain.interfaces.notification_provider import INotificationProvider


class EmailNotificationProvider(INotificationProvider):
    """
    Email Notification Provider (SMTP / SendGrid Async Client).
    """

    def __init__(self, smtp_host: str = "smtp.company.com", smtp_port: int = 587):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    async def send_alert(self, title: str, message: str, severity: str, metadata: Optional[Dict[str, Any]] = None) -> bool:
        # Mock production dispatch
        return True

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    async def send_report(self, report_title: str, report_markdown: str, recipient: str) -> bool:
        # Mock production digest dispatch
        return True
