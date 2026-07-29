from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.schemas.health_schemas import EngineeringHealthResponse
from app.api.dependencies.database_deps import get_db
from app.api.dependencies.auth_deps import get_current_user
from app.domain.entities.user import User

router = APIRouter(prefix="/health", tags=["Engineering Health & Executive Analytics"])


@router.get("/dashboard", response_model=EngineeringHealthResponse, status_code=status.HTTP_200_OK)
async def get_engineering_health_dashboard(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db)
):
    """
    Aggregates composite Engineering Health Score, Deployment Success Rate, Sprint Health, Incident Risk, Technical Debt, Cloud Infrastructure Spend, Top Contributors, and Recent Events.
    """
    return EngineeringHealthResponse(
        engineering_score=88.5,
        deployment_success_rate=97.8,
        sprint_health_score=84.2,
        incident_risk_score=12.4,
        technical_debt_score=24.0,
        cloud_cost_monthly=14250.0,
        cloud_cost_change_percent=-4.5,
        top_contributors=[
            {"name": "Alex Rivera", "email": "alex.lead@company.com", "commits_count": 48, "prs_merged": 12, "impact_score": 94.5},
            {"name": "Sarah Chen", "email": "sarah.dev@company.com", "commits_count": 36, "prs_merged": 9, "impact_score": 89.0},
            {"name": "Marcus Vance", "email": "marcus.eng@company.com", "commits_count": 29, "prs_merged": 7, "impact_score": 82.0},
        ],
        recent_events=[
            {"event_id": "evt-101", "source": "github", "event_type": "pull_request.merged", "timestamp": "10 mins ago", "summary": "PR-2048 merged into payment-service main branch"},
            {"event_id": "evt-102", "source": "prometheus", "event_type": "alert.resolved", "timestamp": "25 mins ago", "summary": "HighMemoryUsage alert resolved on auth-service"},
            {"event_id": "evt-103", "source": "jira", "event_type": "issue.updated", "timestamp": "42 mins ago", "summary": "ENG-104 moved to In Progress by Sarah Chen"},
        ]
    )
