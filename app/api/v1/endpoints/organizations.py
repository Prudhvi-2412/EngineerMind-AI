from fastapi import APIRouter, Depends, HTTPException, status
from app.api.schemas.org_schemas import OrganizationResponse
from app.domain.entities.user import User
from app.infrastructure.persistence.postgres.repositories.postgres_organization_repository import PostgresOrganizationRepository
from app.api.dependencies.service_deps import get_org_repo
from app.api.dependencies.auth_deps import get_current_user

router = APIRouter(prefix="/organizations", tags=["Organization Management"])


@router.get("/me", response_model=OrganizationResponse)
async def get_my_organization(
    current_user: User = Depends(get_current_user),
    org_repo: PostgresOrganizationRepository = Depends(get_org_repo)
):
    """
    Get organization profile of current authenticated user.
    """
    org = await org_repo.get_by_id(current_user.org_id)
    if not org:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")
    return org
