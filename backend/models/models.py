# Python standard library imports
from enum import Enum
from typing import List, Optional

# Third-party package imports
from pydantic import BaseModel, field_validator

# Local imports
# (none in this file)


class ChatRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

    @field_validator("role")
    def validate_role(cls, value):
        if value not in [cls.USER, cls.ASSISTANT, cls.SYSTEM]:
            raise ValueError(f"Role must be one of: {cls.USER}, {cls.ASSISTANT}, {cls.SYSTEM}")
        return value

# Pydantic models for request/response
class GenerateRequest(BaseModel):
    prompt: str
    max_length: Optional[int] = 256
    temperature: Optional[float] = 0.7
    top_p: Optional[float] = 0.9

    @field_validator("prompt")
    def validate_prompt(cls, value):
        if not isinstance(value, str) or len(value.strip()) > 256 or len(value.strip()) <= 0:
            raise ValueError("Prompt must be a non-empty string.")
        return value.strip()

    @field_validator("max_length")
    @classmethod
    def validate_max_length(cls, value):
        if value is not None:
            if value < 1 or value > 1024:  # Reasonable bounds
                raise ValueError("max_length must be between 1 and 1024")
        return value


class ChatMessage(BaseModel):
    role: ChatRole
    content: str

    @field_validator("content")
    @classmethod
    def validate_content(cls, value):
        if not isinstance(value, str):
            raise ValueError("Content must be a string")
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Content cannot be empty")
        if len(cleaned) > 4000:  # Reasonable limit
            raise ValueError("Content too long (max 4000 characters)")
        return cleaned


class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    max_length: Optional[int] = 256
    temperature: Optional[float] = 0.7
    conversation_id: Optional[str] = None
    user_id: Optional[str] = None

    @field_validator("messages")
    @classmethod
    def validate_messages(cls, value):
        if not isinstance(value, list):
            raise ValueError("Messages must be a list")
        if not value:
            raise ValueError("Messages list cannot be empty")
        for msg in value:
            if not isinstance(msg, ChatMessage):
                raise ValueError("All messages must be ChatMessage instances")
        return value


class GenerateResponse(BaseModel):
    generated_text: str
    prompt: str


class ChatResponse(BaseModel):
    response: str
    conversation_id: str


class ConversationRequest(BaseModel):
    user_id: Optional[str] = None
    title: Optional[str] = None


class ConversationResponse(BaseModel):
    conversation_id: str
    title: Optional[str] = None
    created_at: str
