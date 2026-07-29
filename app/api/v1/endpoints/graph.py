from fastapi import APIRouter, Depends, HTTPException, status
from neo4j import AsyncSession
from app.api.schemas.graph_schemas import SyncPRGraphRequest, BlastRadiusResponse, RootCauseResponse
from app.infrastructure.persistence.neo4j.connection import get_neo4j_session
from app.infrastructure.persistence.neo4j.repositories.neo4j_graph_repository import Neo4jGraphRepository
from app.application.services.graph_sync_service import GraphSyncService
from app.api.dependencies.auth_deps import get_current_user
from app.domain.entities.user import User

router = APIRouter(prefix="/graph", tags=["Neo4j Knowledge Graph & Risk Analytics"])


@router.post("/sync/pr", status_code=status.HTTP_201_CREATED)
async def sync_pr_to_graph(
    payload: SyncPRGraphRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_neo4j_session)
):
    """
    Sync a Pull Request entity and touched microservices into the Neo4j Knowledge Graph.
    """
    service = GraphSyncService(session)
    await service.sync_pull_request_event(
        pr_id=payload.pr_id,
        title=payload.title,
        author_email=payload.author_email,
        author_name=payload.author_name,
        repo_full_name=payload.repo_full_name,
        touched_services=payload.touched_services
    )
    return {"status": "synced", "pr_id": payload.pr_id}


@router.get("/prs/{pr_id}/blast-radius", response_model=BlastRadiusResponse)
async def get_pr_blast_radius(
    pr_id: str,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_neo4j_session)
):
    """
    Calculate the architectural blast radius of a PR across microservices, databases, and downstream services.
    """
    repo = Neo4jGraphRepository(session)
    result = await repo.get_pr_blast_radius(pr_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"PR '{pr_id}' not found in Knowledge Graph"
        )
    return result


@router.get("/incidents/{incident_id}/root-cause", response_model=RootCauseResponse)
async def get_incident_root_cause(
    incident_id: str,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_neo4j_session)
):
    """
    Trace an incident back through deployment, PR, and developer author in the Neo4j Knowledge Graph.
    """
    repo = Neo4jGraphRepository(session)
    result = await repo.get_incident_root_cause(incident_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Incident '{incident_id}' not found in Knowledge Graph"
        )
    return result
