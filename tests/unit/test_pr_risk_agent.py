import pytest
from app.application.agents.pr_risk_agent import build_pr_risk_agent


@pytest.mark.asyncio
async def test_pr_risk_agent_execution():
    agent = build_pr_risk_agent()

    initial_state = {
        "pr_id": "PR-999",
        "repo_name": "acme/auth-service",
        "pr_title": "Update DB pool size and OAuth callback",
        "author_email": "lead@company.com",
        "additions": 350,
        "deletions": 120,
        "changed_files": 12,
        "commit_shas": ["commit1", "commit2"],
        "neo4j_session": None,
        "neo4j_blast_radius": {},
        "developer_history": {},
        "risk_score": 0.0,
        "risk_level": "LOW",
        "reasoning": [],
        "evidence": [],
        "suggested_reviewers": []
    }

    final_state = await agent.ainvoke(initial_state)

    assert "risk_score" in final_state
    assert isinstance(final_state["risk_score"], float)
    assert final_state["risk_level"] in ("LOW", "MEDIUM", "HIGH", "CRITICAL")
    assert len(final_state["reasoning"]) > 0
    assert len(final_state["suggested_reviewers"]) > 0
