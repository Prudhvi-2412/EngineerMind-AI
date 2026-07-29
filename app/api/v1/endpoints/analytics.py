import io
import csv
from fastapi import APIRouter, Depends, Query, status, Response
from fastapi.responses import StreamingResponse
from app.api.schemas.analytics_schemas import AnalyticsTimeSeriesResponse
from app.api.dependencies.auth_deps import get_current_user
from app.domain.entities.user import User

router = APIRouter(prefix="/analytics", tags=["Engineering Analytics, Trends & Report Export"])


@router.get("/trends", response_model=AnalyticsTimeSeriesResponse, status_code=status.HTTP_200_OK)
async def get_analytics_trends(
    timeframe: str = Query("30d", enum=["30d", "90d", "1y"]),
    current_user: User = Depends(get_current_user)
):
    """
    Returns time-series telemetry metrics for Velocity, Deployment Frequency, MTTR, Lead Time, Bug Trends, and Engineering Score.
    """
    dates = ["Jul 01", "Jul 05", "Jul 10", "Jul 15", "Jul 20", "Jul 25", "Jul 30"]

    return AnalyticsTimeSeriesResponse(
        timeframe=timeframe,
        velocity_trend=[{"date": d, "story_points": pts} for d, pts in zip(dates, [38, 42, 45, 40, 48, 52, 50])],
        deployment_frequency_trend=[{"date": d, "deployments": dep} for d, dep in zip(dates, [3, 4, 5, 2, 6, 4, 5])],
        mttr_trend=[{"date": d, "mttr_minutes": mttr} for d, mttr in zip(dates, [35, 28, 22, 19, 18, 16, 15])],
        lead_time_trend=[{"date": d, "lead_time_hours": lt} for d, lt in zip(dates, [3.2, 2.8, 2.5, 2.1, 1.9, 1.8, 1.7])],
        bug_trends=[{"date": d, "opened": o, "resolved": r} for d, o, r in zip(dates, [5, 4, 3, 6, 2, 1, 2], [6, 5, 4, 7, 4, 3, 4])],
        engineering_score_trend=[{"date": d, "score": s} for d, s in zip(dates, [81.0, 83.5, 85.0, 84.2, 87.0, 88.5, 89.2])]
    )


@router.get("/export/csv", status_code=status.HTTP_200_OK)
async def export_analytics_csv(
    timeframe: str = Query("30d", enum=["30d", "90d", "1y"]),
    current_user: User = Depends(get_current_user)
):
    """
    Exports Engineering Analytics time-series dataset as a downloadable CSV spreadsheet.
    """
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Date", "Velocity (Story Points)", "Deployments", "MTTR (mins)", "Lead Time (hrs)", "Bugs Opened", "Bugs Resolved", "Engineering Score"])

    dates = ["2026-07-01", "2026-07-05", "2026-07-10", "2026-07-15", "2026-07-20", "2026-07-25", "2026-07-30"]
    for i, d in enumerate(dates):
        writer.writerow([d, 38 + i * 2, 3 + (i % 3), 35 - i * 3, round(3.2 - i * 0.2, 1), 5 - (i % 2), 6 - (i % 2), round(81.0 + i * 1.3, 1)])

    output.seek(0)
    headers = {"Content-Disposition": f"attachment; filename=engineering_analytics_{timeframe}.csv"}
    return StreamingResponse(io.BytesIO(output.getvalue().encode()), media_type="text/csv", headers=headers)


@router.get("/export/pdf", status_code=status.HTTP_200_OK)
async def export_analytics_pdf(
    timeframe: str = Query("30d", enum=["30d", "90d", "1y"]),
    current_user: User = Depends(get_current_user)
):
    """
    Exports Executive Engineering Analytics Summary as a downloadable PDF document.
    """
    pdf_bytes = b"%PDF-1.4 Mock EngineeringOS Executive Analytics PDF Report Document"
    headers = {"Content-Disposition": f"attachment; filename=executive_analytics_{timeframe}.pdf"}
    return Response(content=pdf_bytes, media_type="application/pdf", headers=headers)
