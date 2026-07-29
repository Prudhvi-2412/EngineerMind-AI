from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.persistence.postgres.connection import get_async_db

# Re-export for DI readability
get_db = get_async_db
