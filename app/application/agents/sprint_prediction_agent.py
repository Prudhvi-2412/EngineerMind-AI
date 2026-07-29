from typing import TypedDict, List, Dict, Any, Optional
import json
from langgraph.graph import StateGraph, END
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
from app.core.config import settings


class SprintPredictionState(TypedDict):
    # Inputs
    sprint_id: str
    sprint_name: str
    total_story_points: float
    completed_story_points: float
    days_remaining: int
    historical_team_velocity: float
    blocked_tasks_count: int
    blocked_tasks_details: List[Dict[str, Any]]

    # Intermediate Analytics
    remaining_story_points: float
    required_daily_velocity: float
    burndown_trend_slope: float
    velocity_deficit_ratio: float

    # Agent Outputs
    sprint_success_percentage: float
    delay_probability: float
    reasons: List[str]
    recommendations: List[str]


async def node_calculate_velocity_burndown_metrics(state: SprintPredictionState) -> Dict[str, Any]:
    """
    Node 1: Calculates burndown trajectory, velocity deficit ratio, and required daily points
    """
    remaining_points = max(0.0, state["total_story_points"] - state["completed_story_points"])
    days = max(1, state["days_remaining"])

    required_daily_vel = remaining_points / days
    historical_daily_vel = max(0.1, state["historical_team_velocity"] / 10.0) # assuming 10-day sprint baseline

    deficit_ratio = required_daily_vel / historical_daily_vel

    # Burndown slope: negative value indicates points remaining reduction per day
    burndown_slope = -required_daily_vel

    return {
        "remaining_story_points": remaining_points,
        "required_daily_velocity": round(required_daily_vel, 2),
        "burndown_trend_slope": round(burndown_slope, 2),
        "velocity_deficit_ratio": round(deficit_ratio, 2)
    }


async def node_analyze_blocked_tasks_impact(state: SprintPredictionState) -> Dict[str, Any]:
    """
    Node 2: Evaluates risk impact of blocked Jira tickets & dependency friction
    """
    blocked_count = state["blocked_tasks_count"]
    blocked_details = state.get("blocked_tasks_details", [])

    total_blocked_points = sum(task.get("story_points", 3) for task in blocked_details)
    blocked_ratio = total_blocked_points / max(1.0, state["total_story_points"])

    return {
        "blocked_tasks_details": blocked_details,
        "blocked_ratio": round(blocked_ratio, 2)
    }


async def node_llm_sprint_synthesis(state: SprintPredictionState) -> Dict[str, Any]:
    """
    Node 3: OpenAI LLM Sprint Prediction Synthesizer
    """
    remaining_pts = state["remaining_story_points"]
    req_vel = state["required_daily_velocity"]
    hist_vel = state["historical_team_velocity"]
    deficit = state["velocity_deficit_ratio"]
    blocked_cnt = state["blocked_tasks_count"]
    days_left = state["days_remaining"]

    prompt = f"""
You are the Agile Engineering Manager & AI Data Scientist for EngineeringOS AI.
Analyze the following active Jira Sprint telemetry to predict Sprint Success % and Delay Probability %.

--- SPRINT TELEMETRY ---
Sprint Name: {state['sprint_name']} (ID: {state['sprint_id']})
Total Sprint Story Points: {state['total_story_points']}
Completed Story Points: {state['completed_story_points']}
Remaining Story Points: {remaining_pts}
Days Remaining in Sprint: {days_left}
Historical Team Velocity (per sprint): {hist_vel}
Required Daily Velocity: {req_vel} pts/day
Velocity Deficit Ratio (Required / Historical): {deficit}
Blocked Tasks Count: {blocked_cnt}

Generate a JSON response with:
1. "sprint_success_percentage": Float (0.0 to 100.0).
2. "delay_probability": Float (0.0 to 100.0).
3. "reasons": Array of clear root cause explanation strings.
4. "recommendations": Array of actionable sprint adjustment recommendations.

Respond ONLY in valid JSON:
{{
  "sprint_success_percentage": <float>,
  "delay_probability": <float>,
  "reasons": ["<reason_1>", "<reason_2>"],
  "recommendations": ["<rec_1>", "<rec_2>"]
}}
"""

    try:
        llm = ChatOpenAI(
            model=settings.OPENAI_MODEL,
            openai_api_key=settings.OPENAI_API_KEY,
            temperature=0.1
        )
        response = await llm.ainvoke([
            SystemMessage(content="You produce structured JSON sprint completion predictions."),
            HumanMessage(content=prompt)
        ])
        content = response.content.strip()
        if content.startswith("```json"):
            content = content.split("```json")[1].split("```")[0].strip()
        result = json.loads(content)
    except Exception as e:
        # Fallback Evaluator if OpenAI API is offline
        if deficit > 1.5 or blocked_cnt >= 3:
            success = max(20.0, 100.0 - (deficit * 25.0) - (blocked_cnt * 10.0))
            delay = min(95.0, 100.0 - success)
        else:
            success = min(95.0, 100.0 - (deficit * 10.0))
            delay = max(5.0, 100.0 - success)

        result = {
            "sprint_success_percentage": round(success, 1),
            "delay_probability": round(delay, 1),
            "reasons": [
                f"Required daily velocity ({req_vel} pts/day) exceeds historical team baseline.",
                f"Active blockages on {blocked_cnt} Jira tasks consuming capacity."
            ],
            "recommendations": [
                "Unblock high-priority Jira dependencies in tomorrow's standup.",
                "Descope non-critical story points to preserve sprint commitment."
            ]
        }

    return {
        "sprint_success_percentage": result["sprint_success_percentage"],
        "delay_probability": result["delay_probability"],
        "reasons": result["reasons"],
        "recommendations": result["recommendations"]
    }


def build_sprint_prediction_agent():
    """
    Constructs and compiles the LangGraph StateGraph agent for Sprint Prediction.
    """
    workflow = StateGraph(SprintPredictionState)

    workflow.add_node("calculate_velocity_burndown_metrics", node_calculate_velocity_burndown_metrics)
    workflow.add_node("analyze_blocked_tasks_impact", node_analyze_blocked_tasks_impact)
    workflow.add_node("llm_sprint_synthesis", node_llm_sprint_synthesis)

    workflow.set_entry_point("calculate_velocity_burndown_metrics")
    workflow.add_edge("calculate_velocity_burndown_metrics", "analyze_blocked_tasks_impact")
    workflow.add_edge("analyze_blocked_tasks_impact", "llm_sprint_synthesis")
    workflow.add_edge("llm_sprint_synthesis", END)

    return workflow.compile()
