import pytest
from app.application.agents.developer_insight_agent import build_developer_insight_agent


@pytest.mark.asyncio
async def test_developer_insight_agent_execution():
    agent = build_developer_insight_agent()

    initial_state = {
        "developer_email": "engineer@company.com",
        "time_window_days": 30,
        "neo4j_session": None,
        "code_ownership_matrix": {},
        "domain_expertise_tags": [],
        "knowledge_distribution_score": 0.0,
        "review_quality_score": 0.0,
        "weekly_workload_hours": 0.0,
        "late_night_commit_count": 0,
        "weekend_commit_count": 0,
        "burnout_risk_score": 0.0,
        "burnout_risk_level": "LOW",
        "burnout_indicators": [],
        "insights_summary": "",
        "recommendations": []
    }

    final_state = await agent.ainvoke(initial_state)

    assert "burnout_risk_score" in final_state
    assert isinstance(final_state["burnout_risk_score"], float)
    assert final_state["burnout_risk_level"] in ("LOW", "MEDIUM", "HIGH", "CRITICAL")
    assert "code_ownership_matrix" in final_state
    assert "domain_expertise_tags" in final_state
    assert len(final_state["insights_summary"]) > 0
    assert len(final_state["recommendations"]) > 0
