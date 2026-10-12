from typing import Optional, Dict, Any
from pydantic import BaseModel


class ChatMessagePayload(BaseModel):
    sessionId: str
    sender: str
    message: str
    role: Optional[str] = "patient"


class ChatAskRequest(BaseModel):
    sessionId: Optional[str] = None
    message: str
    context: Optional[Dict[str, Any]] = None
