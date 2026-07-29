from typing import List, Dict, Any
from pydantic import BaseModel, Field


class AnalyticsTimeSeriesResponse(BaseModel):
    timeframe: str = Field("30d", example="30d")
    velocity_trend: List[Dict[str, Any]] = Field(..., example=[{"date": "2026-07-01", "story_points": 42.0}])
    deployment_frequency_trend: List[Dict[str, Any]] = Field(..., example=[{"date": "2026-07-01", "deployments": 4}])
    mttr_trend: List[Dict[str, Any]] = Field(..., example=[{"date": "2026-07-01", "mttr_minutes": 18.5}])
    lead_time_trend: List[Dict[str, Any]] = Field(..., example=[{"date": "2026-07-01", "lead_time_hours": 1.8}])
    bug_trends: List[Dict[str, Any]] = Field(..., example=[{"date": "2026-07-01", "opened": 3, "resolved": 5}])
    engineering_score_trend: List[Dict[str, Any]] = Field(..., example=[{"date": "2026-07-01", "score": 88.5}])
