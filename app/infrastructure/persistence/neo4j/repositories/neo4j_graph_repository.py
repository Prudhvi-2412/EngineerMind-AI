from typing import Dict, Any, List, Optional
from neo4j import AsyncSession


class Neo4jGraphRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    # -------------------------------------------------------------
    # NODE & RELATIONSHIP UPSERTS
    # -------------------------------------------------------------

    async def upsert_developer(self, email: str, name: str, team_name: Optional[str] = None):
        cypher = """
        MERGE (d:Developer {email: $email})
        SET d.name = $name, d.updated_at = timestamp()
        """
        await self.session.run(cypher, email=email, name=name)

        if team_name:
            team_cypher = """
            MATCH (d:Developer {email: $email})
            MERGE (t:Team {name: $team_name})
            MERGE (d)-[:MEMBER_OF]->(t)
            """
            await self.session.run(team_cypher, email=email, team_name=team_name)

    async def upsert_pull_request(
        self,
        pr_id: str,
        title: str,
        author_email: str,
        repo_full_name: str,
        touched_services: List[str]
    ):
        cypher = """
        MERGE (pr:PullRequest {pr_id: $pr_id})
        SET pr.title = $title, pr.updated_at = timestamp()

        MERGE (d:Developer {email: $author_email})
        MERGE (d)-[:CREATED]->(pr)

        MERGE (r:Repository {full_name: $repo_full_name})
        MERGE (pr)-[:BELONGS_TO_REPO]->(r)
        """
        await self.session.run(
            cypher,
            pr_id=pr_id,
            title=title,
            author_email=author_email,
            repo_full_name=repo_full_name
        )

        for service in touched_services:
            touch_cypher = """
            MATCH (pr:PullRequest {pr_id: $pr_id})
            MERGE (s:Microservice {name: $service})
            MERGE (pr)-[:TOUCHES]->(s)
            """
            await self.session.run(touch_cypher, pr_id=pr_id, service=service)

    async def link_service_database(self, service_name: str, db_name: str, db_type: str = "PostgreSQL"):
        cypher = """
        MERGE (s:Microservice {name: $service_name})
        MERGE (db:Database {name: $db_name})
        SET db.type = $db_type
        MERGE (s)-[:USES]->(db)
        """
        await self.session.run(cypher, service_name=service_name, db_name=db_name, db_type=db_type)

    async def record_deployment_and_incident(
        self,
        deployment_id: str,
        pr_id: str,
        service_name: str,
        incident_id: Optional[str] = None,
        incident_title: Optional[str] = None
    ):
        cypher = """
        MERGE (dep:Deployment {deployment_id: $deployment_id})
        SET dep.timestamp = timestamp()

        MATCH (pr:PullRequest {pr_id: $pr_id})
        MERGE (dep)-[:TRIGGERED_BY]->(pr)

        MERGE (s:Microservice {name: $service_name})
        MERGE (dep)-[:DEPLOYED_TO]->(s)
        """
        await self.session.run(cypher, deployment_id=deployment_id, pr_id=pr_id, service_name=service_name)

        if incident_id and incident_title:
            inc_cypher = """
            MATCH (dep:Deployment {deployment_id: $deployment_id})
            MERGE (inc:Incident {incident_id: $incident_id})
            SET inc.title = $incident_title, inc.created_at = timestamp()
            MERGE (dep)-[:CAUSED]->(inc)
            """
            await self.session.run(inc_cypher, deployment_id=deployment_id, incident_id=incident_id, incident_title=incident_title)

    # -------------------------------------------------------------
    # ANALYTIC & GRAPH TRAVERSAL QUERIES
    # -------------------------------------------------------------

    async def get_pr_blast_radius(self, pr_id: str) -> Dict[str, Any]:
        """
        Calculates impact blast radius of a PR across microservices, databases, and historical incidents.
        """
        cypher = """
        MATCH (pr:PullRequest {pr_id: $pr_id})
        OPTIONAL MATCH (dev:Developer)-[:CREATED]->(pr)
        OPTIONAL MATCH (pr)-[:TOUCHES]->(s:Microservice)
        OPTIONAL MATCH (s)-[:USES]->(db:Database)
        OPTIONAL MATCH (other:Microservice)-[:DEPENDS_ON]->(s)
        OPTIONAL MATCH (s)<-[:DEPLOYED_TO]-(dep:Deployment)-[:CAUSED]->(inc:Incident)

        RETURN 
            pr.pr_id as pr_id,
            pr.title as title,
            dev.email as author_email,
            collect(DISTINCT s.name) as touched_services,
            collect(DISTINCT db.name) as databases_at_risk,
            collect(DISTINCT other.name) as dependent_downstream_services,
            collect(DISTINCT inc.title) as historical_incidents
        """
        res = await self.session.run(cypher, pr_id=pr_id)
        record = await res.single()
        if not record:
            return {}
        return dict(record)

    async def get_incident_root_cause(self, incident_id: str) -> Dict[str, Any]:
        """
        Traces an Incident back to the deployment, PR, developer author, and touched microservice.
        """
        cypher = """
        MATCH (inc:Incident {incident_id: $incident_id})<-[:CAUSED]-(dep:Deployment)
        OPTIONAL MATCH (dep)-[:TRIGGERED_BY]->(pr:PullRequest)
        OPTIONAL MATCH (dev:Developer)-[:CREATED]->(pr)
        OPTIONAL MATCH (dep)-[:DEPLOYED_TO]->(s:Microservice)

        RETURN 
            inc.incident_id as incident_id,
            inc.title as incident_title,
            dep.deployment_id as deployment_id,
            pr.pr_id as pr_id,
            pr.title as pr_title,
            dev.name as author_name,
            dev.email as author_email,
            s.name as affected_service
        """
        res = await self.session.run(cypher, incident_id=incident_id)
        record = await res.single()
        if not record:
            return {}
        return dict(record)
