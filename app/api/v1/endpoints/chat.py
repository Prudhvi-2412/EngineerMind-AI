from fastapi import APIRouter, Depends, status
from neo4j import AsyncSession
from sqlalchemy.ext.asyncio import AsyncSession as PGAsyncSession
from app.api.schemas.chat_schemas import ChatMessageRequest, ChatMessageResponse
from app.infrastructure.persistence.neo4j.connection import get_neo4j_session
from app.api.dependencies.database_deps import get_db
from app.api.dependencies.auth_deps import get_current_user
from app.domain.entities.user import User

router = APIRouter(prefix="/chat", tags=["Grounded AI Chat Assistant & Engineering Knowledge RAG"])


@router.post("/message", response_model=ChatMessageResponse, status_code=status.HTTP_200_OK)
async def chat_with_engineering_assistant(
    payload: ChatMessageRequest,
    current_user: User = Depends(get_current_user),
    neo4j_session: AsyncSession = Depends(get_neo4j_session),
    db_session: PGAsyncSession = Depends(get_db)
):
    """
    Execute LangGraph Grounded AI Chat Assistant.
    Grounds questions across Neo4j Knowledge Graph, PostgreSQL telemetry DB, GitHub, and Jira without hallucination.
    """
    from app.application.agents.engineering_chat_agent import build_engineering_chat_agent

    agent = build_engineering_chat_agent()

    initial_state = {
        "user_query": payload.user_query,
        "chat_history": payload.chat_history,
        "neo4j_session": neo4j_session,
        "db_session": db_session,
        "intent_category": "repository",
        "retrieved_graph_context": {},
        "retrieved_db_context": {},
        "grounded_evidence": [],
        "assistant_response": "",
        "confidence_score": 0.0
    }

    final_state = await agent.ainvoke(initial_state)

    return ChatMessageResponse(
        user_query=payload.user_query,
        intent_category=final_state["intent_category"],
        assistant_response=final_state["assistant_response"],
        confidence_score=final_state["confidence_score"],
        grounded_evidence=final_state["grounded_evidence"]
    )
