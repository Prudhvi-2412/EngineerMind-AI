from neo4j import AsyncSession

INIT_CYPHER_CONSTRAINTS = [
    "CREATE CONSTRAINT dev_email IF NOT EXISTS FOR (d:Developer) REQUIRE d.email IS UNIQUE;",
    "CREATE CONSTRAINT repo_fullname IF NOT EXISTS FOR (r:Repository) REQUIRE r.full_name IS UNIQUE;",
    "CREATE CONSTRAINT service_name IF NOT EXISTS FOR (s:Microservice) REQUIRE s.name IS UNIQUE;",
    "CREATE CONSTRAINT pr_id IF NOT EXISTS FOR (pr:PullRequest) REQUIRE pr.pr_id IS UNIQUE;",
    "CREATE CONSTRAINT issue_id IF NOT EXISTS FOR (i:Issue) REQUIRE i.issue_id IS UNIQUE;",
    "CREATE CONSTRAINT deployment_id IF NOT EXISTS FOR (dep:Deployment) REQUIRE dep.deployment_id IS UNIQUE;",
    "CREATE CONSTRAINT incident_id IF NOT EXISTS FOR (inc:Incident) REQUIRE inc.incident_id IS UNIQUE;",
    "CREATE CONSTRAINT team_name IF NOT EXISTS FOR (t:Team) REQUIRE t.name IS UNIQUE;",
]


async def init_neo4j_schema(session: AsyncSession):
    """
    Initializes Neo4j database schema constraints and indexes for high-speed O(1) lookups.
    """
    for query in INIT_CYPHER_CONSTRAINTS:
        try:
            await session.run(query)
        except Exception as e:
            print(f"Warning: Failed to execute schema constraint query '{query}': {e}")
