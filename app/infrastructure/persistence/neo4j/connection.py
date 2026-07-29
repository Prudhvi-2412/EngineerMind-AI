from typing import AsyncGenerator
from neo4j import AsyncGraphDatabase, AsyncDriver, AsyncSession
from app.core.config import settings

class Neo4jConnectionManager:
    _driver: AsyncDriver | None = None

    @classmethod
    def get_driver(cls) -> AsyncDriver:
        if cls._driver is None:
            cls._driver = AsyncGraphDatabase.driver(
                settings.NEO4J_URI,
                auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
            )
        return cls._driver

    @classmethod
    async def close_driver(cls):
        if cls._driver is not None:
            await cls._driver.close()
            cls._driver = None


async def get_neo4j_session() -> AsyncGenerator[AsyncSession, None]:
    driver = Neo4jConnectionManager.get_driver()
    async with driver.session() as session:
        yield session
