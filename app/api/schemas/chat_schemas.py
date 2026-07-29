from typing import List, Dict, Any
from pydantic import BaseModel, Field


class ChatMessageRequest(BaseModel):
    user_query: str = Field(..., example="What is the blast radius of PR-2048 and are any databases at risk?")
    chat_history: List[Dict[str, str]] = Field(default_factory=list, example=[{"role": "user", "content": "Hello"}])


class ChatMessageResponse(BaseModel):
    user_query: str
    intent_category: str
    assistant_response: str
    confidence_score: float
    grounded_evidence: List[Dict[str, Any]]
