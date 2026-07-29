from typing import List, Dict, Any, Optional
import asyncio
from app.domain.interfaces.notification_provider import INotificationProvider
from app.infrastructure.notifications.slack_provider import SlackNotificationProvider
from app.infrastructure.notifications.email_provider import EmailNotificationProvider
from app.infrastructure.notifications.github_comment_provider import GitHubCommentNotificationProvider
from app.infrastructure.notifications.ms_teams_provider import MSTeamsNotificationProvider


class AlertEngine:
    """
    Central Multi-Channel Alert Dispatcher & Operational Risk Engine.
    Dispatches alerts concurrently across Slack, Email, GitHub Comments, and MS Teams with automatic retry logic.
    """

    def __init__(self, providers: Optional[List[INotificationProvider]] = None):
        self.providers = providers or [
            SlackNotificationProvider(),
            EmailNotificationProvider(),
            GitHubCommentNotificationProvider(),
            MSTeamsNotificationProvider()
        ]

    async def dispatch_risk_alert(
        self,
        title: str,
        message: str,
        severity: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, bool]:
        """
        Dispatches risk alert across all active channel providers in parallel.
        """
        results = {}

        tasks = [
            provider.send_alert(title, message, severity, metadata)
            for provider in self.providers
        ]

        responses = await asyncio.gather(*tasks, return_exceptions=True)

        for provider, resp in zip(self.providers, responses):
            provider_name = provider.__class__.__name__
            if isinstance(resp, Exception):
                results[provider_name] = False
            else:
                results[provider_name] = bool(resp)

        return results
