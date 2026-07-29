import pytest
from app.api.schemas.analytics_schemas import AnalyticsTimeSeriesResponse


def test_analytics_schema_validation():
    payload = {
        "timeframe": "30d",
        "velocity_trend": [{"date": "Jul 01", "story_points": 42.0}],
        "deployment_frequency_trend": [{"date": "Jul 01", "deployments": 4}],
        "mttr_trend": [{"date": "Jul 01", "mttr_minutes": 18.5}],
        "lead_time_trend": [{"date": "Jul 01", "lead_time_hours": 1.8}],
        "bug_trends": [{"date": "Jul 01", "opened": 3, "resolved": 5}],
        "engineering_score_trend": [{"date": "Jul 01", "score": 88.5}]
    }

    model = AnalyticsTimeSeriesResponse(**payload)
    assert model.timeframe == "30d"
    assert model.velocity_trend[0]["story_points"] == 42.0
    assert model.bug_trends[0]["opened"] == 3
