import httpx
from typing import Dict, Any, Optional
from tenacity import retry, stop_after_attempt, wait_exponential
from app.domain.interfaces.notification_provider import INotificationProvider


class GitHubCommentNotificationProvider(INotificationProvider):
    """
    GitHub Pull Request Comment Provider for automated PR AI Risk Reviews.
    """

    def __init__(self, github_token: Optional[str] = None):
        self.token = github_token or "ghp_mock_token"

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    async def post_pr_review_comment(self, repo_full_name: str, pr_number: int, comment_body: str) -> bool:
        url = f"https://api.github.com/repos/{repo_full_name}/issues/{pr_number}/comments"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json"
        }
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, json={"body": comment_body}, headers=headers, timeout=5.0)
            return resp.status_code in (200, 201)

    async def send_alert(self, title: str, message: str, severity: str, metadata: Optional[Dict[str, Any]] = None) -> bool:
        if metadata and "repo" in metadata and "pr_number" in metadata:
            comment_body = f"### 🤖 EngineeringOS AI Risk Assessment: {title}\n\n**Severity:** `{severity}`\n\n{message}"
            return await self.post_pr_review_comment(metadata["repo"], metadata["pr_number"], comment_body)
        return True

    async def send_report(self, report_title: str, report_markdown: str, recipient: str) -> bool:
        return True
