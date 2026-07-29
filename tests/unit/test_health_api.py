import pytest
from app.api.schemas.health_schemas import EngineeringHealthResponse


def test_engineering_health_schema_validation():
    payload = {
        "engineering_score": 88.5,
        "deployment_success_rate": 97.8,
        "sprint_health_score": 84.2,
        "incident_risk_score": 12.4,
        "technical_debt_score": 24.0,
        "cloud_cost_monthly": 14250.0,
        "cloud_cost_change_percent": -4.5,
        "top_contributors": [
            {"name": "Alex Rivera", "email": "alex.lead@company.com", "commits_count": 48, "prs_merged": 12, "impact_score": 94.5}
        ],
        "recent_events": [
            {"event_id": "evt-101", "source": "github", "event_type": "pull_request.merged", "timestamp": "10 mins ago", "summary": "PR merged"}
        ]
    }

    model = EngineeringHealthResponse(**payload)
    assert model.engineering_score == 88.5
    assert model.deployment_success_rate == 97.8
    assert len(model.top_contributors) == 1
    assert model.top_contributors[0].name == "Alex Rivera"
