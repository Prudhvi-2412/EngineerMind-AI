import hmac
import hashlib
import pytest
from app.infrastructure.external.github_client import verify_webhook_signature, RateLimitExceededException


def test_verify_webhook_signature_valid():
    secret = "super_secret_webhook_key_12345"
    payload = b'{"ref": "refs/heads/main", "commits": []}'
    
    mac = hmac.new(secret.encode(), msg=payload, digestmod=hashlib.sha256)
    valid_signature = f"sha256={mac.hexdigest()}"

    assert verify_webhook_signature(payload, valid_signature, secret) is True


def test_verify_webhook_signature_invalid():
    secret = "super_secret_webhook_key_12345"
    payload = b'{"ref": "refs/heads/main", "commits": []}'
    invalid_signature = "sha256=invalid_hash_value_12345"

    assert verify_webhook_signature(payload, invalid_signature, secret) is False


def test_rate_limit_exception():
    reset_timestamp = 1700000000
    exc = RateLimitExceededException(reset_timestamp=reset_timestamp)
    assert exc.reset_timestamp == reset_timestamp
    assert "Rate limit exceeded" in str(exc)
