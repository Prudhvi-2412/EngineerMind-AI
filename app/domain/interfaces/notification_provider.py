from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional


class INotificationProvider(ABC):
    """
    Abstract Interface for Multi-Channel Notification Providers.
    """

    @abstractmethod
    async def send_alert(self, title: str, message: str, severity: str, metadata: Optional[Dict[str, Any]] = None) -> bool:
        """
        Send an urgent operational risk alert.
        """
        pass

    @abstractmethod
    async def send_report(self, report_title: str, report_markdown: str, recipient: str) -> bool:
        """
        Send a scheduled Daily or Weekly Digest report.
        """
        pass
