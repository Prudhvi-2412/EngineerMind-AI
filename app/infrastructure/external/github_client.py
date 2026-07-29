import time
import hmac
import hashlib
from typing import Dict, Any, List, Optional
import httpx
from app.core.config import settings


class RateLimitExceededException(Exception):
    def __init__(self, reset_timestamp: int, message: str = "GitHub API Rate limit exceeded"):
        self.reset_timestamp = reset_timestamp
        super().__init__(message)


class GitHubApiClient:
    def __init__(self, token: Optional[str] = None):
        self.token = token
        self.base_url = "https://api.github.com"

    def _get_headers(self) -> Dict[str, str]:
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "EngineeringOS-AI-App",
        }
        if self.token:
            headers["Authorization"] = `Bearer ${self.token}` if self.token.startswith("ghp_") or self.token.startswith("ghs_") else f"Bearer {self.token}"
        return headers

    def _check_rate_limit(self, response: httpx.Response):
        remaining = response.headers.get("X-RateLimit-Remaining")
        reset = response.headers.get("X-RateLimit-Reset")

        if response.status_code in (403, 429) and remaining == "0":
            reset_ts = int(reset) if reset else int(time.time()) + 60
            raise RateLimitExceededException(reset_timestamp=reset_ts)

    async def get_repository(self, owner: str, repo: str) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            res = await client.get(
                f"{self.base_url}/repos/{owner}/{repo}",
                headers=self._get_headers()
            )
            self._check_rate_limit(res)
            res.raise_for_status()
            return res.json()

    async def get_commits(self, owner: str, repo: str, per_page: int = 100) -> List[Dict[str, Any]]:
        async with httpx.AsyncClient() as client:
            res = await client.get(
                f"{self.base_url}/repos/{owner}/{repo}/commits?per_page={per_page}",
                headers=self._get_headers()
            )
            self._check_rate_limit(res)
            res.raise_for_status()
            return res.json()

    async def get_pull_requests(self, owner: str, repo: str, state: str = "all") -> List[Dict[str, Any]]:
        async with httpx.AsyncClient() as client:
            res = await client.get(
                f"{self.base_url}/repos/{owner}/{repo}/pulls?state={state}&per_page=100",
                headers=self._get_headers()
            )
            self._check_rate_limit(res)
            res.raise_for_status()
            return res.json()

    async def get_issues(self, owner: str, repo: str, state: str = "all") -> List[Dict[str, Any]]:
        async with httpx.AsyncClient() as client:
            res = await client.get(
                f"{self.base_url}/repos/{owner}/{repo}/issues?state={state}&per_page=100",
                headers=self._get_headers()
            )
            self._check_rate_limit(res)
            res.raise_for_status()
            # Filter out PRs which GitHub includes in issues endpoint
            issues = [i for i in res.json() if "pull_request" not in i]
            return issues


def verify_webhook_signature(payload_body: bytes, signature_header: str, secret: str) -> bool:
    """
    Verifies GitHub Webhook HMAC-SHA256 signature (X-Hub-Signature-256)
    """
    if not signature_header or not signature_header.startswith("sha256="):
        return False

    expected_signature = signature_header.split("sha256=")[1]
    mac = hmac.new(secret.encode(), msg=payload_body, digestmod=hashlib.sha256)
    computed_signature = mac.hexdigest()

    return hmac.compare_digest(computed_signature, expected_signature)
