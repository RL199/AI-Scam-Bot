from pydantic import BaseModel
from typing import Optional, List


# Pydantic models for request/response
class GenerateRequest(BaseModel):
    prompt: str
    max_length: Optional[int] = 256
    temperature: Optional[float] = 0.7
    top_p: Optional[float] = 0.9


class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str


class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    max_length: Optional[int] = 256
    temperature: Optional[float] = 0.7


class GenerateResponse(BaseModel):
    generated_text: str
    prompt: str


class ChatResponse(BaseModel):
    response: str
    conversation_id: Optional[str] = None
