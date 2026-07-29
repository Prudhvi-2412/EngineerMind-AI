from typing import List, Optional
from neo4j import AsyncSession
from app.infrastructure.persistence.neo4j.repositories.neo4j_graph_repository import Neo4jGraphRepository


class GraphSyncService:
    def __init__(self, session: AsyncSession):
        self.graph_repo = Neo4jGraphRepository(session)

    async def sync_pull_request_event(
        self,
        pr_id: str,
        title: str,
        author_email: str,
        author_name: str,
        repo_full_name: str,
        touched_services: List[str]
    ):
        # 1. Upsert Developer
        await self.graph_repo.upsert_developer(email=author_email, name=author_name)
        # 2. Upsert Pull Request & link TOUCHES to Microservices
        await self.graph_repo.upsert_pull_request(
            pr_id=pr_id,
            title=title,
            author_email=author_email,
            repo_full_name=repo_full_name,
            touched_services=touched_services
        )

    async def sync_deployment_incident_event(
        self,
        deployment_id: str,
        pr_id: str,
        service_name: str,
        incident_id: Optional[str] = None,
        incident_title: Optional[str] = None
    ):
        await self.graph_repo.record_deployment_and_incident(
            deployment_id=deployment_id,
            pr_id=pr_id,
            service_name=service_name,
            incident_id=incident_id,
            incident_title=incident_title
        )
