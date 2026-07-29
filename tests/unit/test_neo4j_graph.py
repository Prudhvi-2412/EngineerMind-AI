from unittest.mock import AsyncMock, MagicMock
import pytest
from app.infrastructure.persistence.neo4j.repositories.neo4j_graph_repository import Neo4jGraphRepository


@pytest.mark.asyncio
async def test_neo4j_upsert_developer():
    mock_session = AsyncMock()
    repo = Neo4jGraphRepository(mock_session)

    await repo.upsert_developer("dev@company.com", "Dev Name", "Platform Team")

    assert mock_session.run.call_count == 2


@pytest.mark.asyncio
async def test_neo4j_get_pr_blast_radius():
    mock_session = AsyncMock()
    mock_result = AsyncMock()
    mock_record = {
        "pr_id": "PR-100",
        "title": "Update Auth API",
        "author_email": "dev@company.com",
        "touched_services": ["auth-service", "user-service"],
        "databases_at_risk": ["auth_db"],
        "dependent_downstream_services": ["gateway-service"],
        "historical_incidents": []
    }
    mock_result.single.return_value = mock_record
    mock_session.run.return_value = mock_result

    repo = Neo4jGraphRepository(mock_session)
    radius = await repo.get_pr_blast_radius("PR-100")

    assert radius["pr_id"] == "PR-100"
    assert "auth-service" in radius["touched_services"]
    assert "auth_db" in radius["databases_at_risk"]
