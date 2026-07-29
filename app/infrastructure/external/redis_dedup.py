import redis.asyncio as redis
from app.core.config import settings

redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)


async def is_duplicate_event(delivery_id: str, ttl_seconds: int = 86400) -> bool:
    """
    Checks if a webhook delivery_id has already been received within TTL (24 hours).
    Uses Redis atomic SETNX for ultra-fast distributed lock & deduplication.
    """
    key = f"event_dedup:{delivery_id}"
    # SET key value NX EX seconds -> Returns True if set (new event), None/False if already set (duplicate)
    is_new = await redis_client.set(name=key, value="1", nx=True, ex=ttl_seconds)
    return not is_new
