import pytest
from app.application.agents.sprint_prediction_agent import build_sprint_prediction_agent


@pytest.mark.asyncio
async def test_sprint_prediction_agent_execution():
    agent = build_sprint_prediction_agent()

    initial_state = {
        "sprint_id": "SPRINT-42",
        "sprint_name": "Sprint 42 - Q3 Payment Engine",
        "total_story_points": 80.0,
        "completed_story_points": 25.0,
        "days_remaining": 3,
        "historical_team_velocity": 40.0,
        "blocked_tasks_count": 3,
        "blocked_tasks_details": [{"key": "ENG-104", "story_points": 8}],
        "remaining_story_points": 0.0,
        "required_daily_velocity": 0.0,
        "burndown_trend_slope": 0.0,
        "velocity_deficit_ratio": 1.0,
        "sprint_success_percentage": 0.0,
        "delay_probability": 0.0,
        "reasons": [],
        "recommendations": []
    }

    final_state = await agent.ainvoke(initial_state)

    assert "sprint_success_percentage" in final_state
    assert isinstance(final_state["sprint_success_percentage"], float)
    assert "delay_probability" in final_state
    assert isinstance(final_state["delay_probability"], float)
    assert len(final_state["reasons"]) > 0
    assert len(final_state["recommendations"]) > 0
