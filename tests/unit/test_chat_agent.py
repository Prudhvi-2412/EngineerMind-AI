import pytest
from app.application.agents.engineering_chat_agent import build_engineering_chat_agent


@pytest.mark.asyncio
async def test_engineering_chat_agent_execution():
    agent = build_engineering_chat_agent()

    initial_state = {
        "user_query": "What is the blast radius of PR-2048 and are any databases at risk?",
        "chat_history": [],
        "neo4j_session": None,
        "db_session": None,
        "intent_category": "repository",
        "retrieved_graph_context": {},
        "retrieved_db_context": {},
        "grounded_evidence": [],
        "assistant_response": "",
        "confidence_score": 0.0
    }

    final_state = await agent.ainvoke(initial_state)

    assert "assistant_response" in final_state
    assert len(final_state["assistant_response"]) > 0
    assert len(final_state["grounded_evidence"]) > 0
    assert final_state["confidence_score"] > 90.0
