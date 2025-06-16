from pydantic import BaseModel, validate
from typing import Optional, List


# Pydantic models for request/response
class GenerateRequest(BaseModel):
    prompt: str
    #max_length: Optional[int] = 256 #TODO : check if this is something that need to be accepted by the user
    temperature: Optional[float] = 0.7
    top_p: Optional[float] = 0.9

    @validate("prompt")
    def validate_prompt(cls, value):
        if not isinstance(value, str) or len(value.strip()) > 256 or len(value.strip()) <= 0:
            raise ValueError("Prompt must be a non-empty string.")
        return value


class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str

    # TODO add validation for role and content


class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    temperature: Optional[float] = 0.7

    # TODO add validation for messages


class GenerateResponse(BaseModel):
    generated_text: str
    prompt: str



class ChatResponse(BaseModel):
    response: str
