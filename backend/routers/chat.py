from fastapi import APIRouter
from models.chat import ChatMessagePayload, ChatAskRequest
from services import chat_service

router = APIRouter(prefix="/api/chat", tags=["AI Clinical Chat"])


@router.post("/ask")
def ask_ai(payload: ChatAskRequest):
    """Generate an AI healthcare assistant response via OpenRouter with context awareness."""
    return chat_service.generate_ai_reply(
        session_id=payload.sessionId,
        user_message=payload.message,
        context=payload.context
    )


@router.get("/history")
def get_chat_history(sessionId: str):
    return chat_service.get_chat_history(sessionId)


@router.post("/message")
def post_chat_message(payload: ChatMessagePayload):
    return chat_service.save_chat_message(payload.sessionId, payload.sender, payload.message, payload.role or "patient")


@router.delete("/history")
def clear_chat_history(sessionId: str):
    return chat_service.clear_chat_history(sessionId)
