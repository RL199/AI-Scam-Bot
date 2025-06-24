from functools import wraps
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from contextlib import asynccontextmanager

from datetime import datetime

from models.models import (
    GenerateResponse,
    GenerateRequest,
    ChatResponse,
    ChatRequest,
    ConversationRequest,
    ConversationResponse,
)
import uvicorn
import logging
import time

from model import LLMModel
from database.database import DatabaseManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Default values for model parameters
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_LENGTH = 256


def validate_model(func):
    """Decorator to validate that the LLM model is loaded before executing the endpoint"""

    @wraps(func)
    async def wrapper(*args, **kwargs):
        global llm_model
        if not llm_model or not llm_model.is_loaded():
            raise HTTPException(status_code=503, detail="Model not loaded")
        return await func(*args, **kwargs)

    return wrapper


def ensure_db_manager():
    """Helper function to ensure database manager is initialized"""
    global db_manager
    if db_manager is None:
        raise HTTPException(status_code=500, detail="Database manager not initialized")
    return db_manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    """Initialize the LLM model and database on startup"""
    global llm_model, db_manager
    try:
        logger.info("Loading LLM model...")
        llm_model = LLMModel()
        await llm_model.load_model()
        logger.info("Model loaded successfully")

        # Initialize database
        logger.info("Connecting to database...")
        db_manager = DatabaseManager()
        await db_manager.connect()
        logger.info("Database connected successfully")
    except Exception as e:
        logger.error(f"Failed to initialize services: {e}")
        raise

    yield

    if llm_model:
        await llm_model.cleanup()
    if db_manager:
        await db_manager.disconnect()


app = FastAPI(title="AI Scam Bot API", version="1.0.0", lifespan=lifespan)

# Configure CORS
# Configure allowed origins based on environment
ALLOWED_ORIGINS = [
    "http://localhost:3000",  # Local development
    "https://your-frontend-domain.com",  # Production frontend
]


@app.get("/health")
async def health_check():
    global llm_model
    if llm_model and llm_model.is_loaded():
        return {"status": "healthy", "model_status": "loaded", "api_version": "1.0.0"}
    raise HTTPException(status_code=503, detail="Model not loaded")


async def root():
    return {"message": "AI Scam Bot API is running", "status": "healthy"}


@app.post("/chat", response_model=ChatResponse)
@validate_model
async def chat(request: ChatRequest):
    """Chat with the model using conversation history"""
    global llm_model

    try:
        start_time = time.time()
        db = ensure_db_manager()

        # Set default values once
        temperature = (
            DEFAULT_TEMPERATURE if request.temperature is None else request.temperature
        )
        max_length = (
            DEFAULT_MAX_LENGTH if request.max_length is None else request.max_length
        )

        # Create conversation if not provided
        conversation_id = request.conversation_id
        if not conversation_id:
            conversation_id = await db.create_conversation(
                user_id=request.user_id, title=f"Chat {len(request.messages)} messages"
            )

        # Save user messages to database
        for msg in request.messages:
            if msg.role == "user":
                await db.save_message(
                    conversation_id=conversation_id, role=msg.role, content=msg.content
                )

        if llm_model is None:
            raise HTTPException(status_code=500, detail="LLM model not initialized")

        messages_dict = [
            {"role": msg.role, "content": msg.content} for msg in request.messages
        ]

        response = await llm_model.chat(
            messages=messages_dict,
            max_length=max_length,
            temperature=temperature,
        )

        # Save assistant response to database
        await db.save_message(
            conversation_id=conversation_id, role="assistant", content=response
        )

        # Save interaction statistics
        generation_time = int((time.time() - start_time) * 1000)
        await db.save_interaction_stats(
            conversation_id=conversation_id,
            generation_time_ms=generation_time,
            model_name=llm_model.model_name,
            temperature=temperature,
            max_length=max_length,
        )

        return ChatResponse(response=response, conversation_id=conversation_id)
    except Exception as error:
        logger.error(f"Chat error: {error}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Chat failed: {error}")


@app.post("/conversations", response_model=ConversationResponse)
async def create_conversation(request: ConversationRequest):
    """Create a new conversation"""
    try:
        db = ensure_db_manager()
        conversation_id = await db.create_conversation(
            user_id=request.user_id, title=request.title
        )

        return ConversationResponse(
            conversation_id=conversation_id,
            title=request.title,
            created_at=datetime.utcnow().isoformat(),
        )
    except Exception as e:
        logger.error(f"Error creating conversation: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to create conversation: {str(e)}"
        )


@app.get("/conversations/{conversation_id}/history")
async def get_conversation_history(conversation_id: str, limit: int = 50):
    """Get conversation history"""
    try:
        db = ensure_db_manager()
        history = await db.get_conversation_history(conversation_id, limit)
        return {"conversation_id": conversation_id, "messages": history}
    except Exception as e:
        logger.error(f"Error getting conversation history: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get history: {str(e)}")


@app.get("/users/{user_id}/conversations")
async def get_user_conversations(user_id: str, limit: int = 20):
    """Get user's conversations"""
    try:
        db = ensure_db_manager()
        conversations = await db.get_user_conversations(user_id, limit)
        return {"user_id": user_id, "conversations": conversations}
    except Exception as e:
        logger.error(f"Error getting user conversations: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to get conversations: {str(e)}"
        )


@app.get("/model/info")
@validate_model
async def model_info():
    """Get information about the loaded model"""
    global llm_model
    if llm_model is None:
        raise HTTPException(status_code=500, detail="LLM model not initialized")
    return await llm_model.get_model_info()


if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
