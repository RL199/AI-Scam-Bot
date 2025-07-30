# Python standard library imports
import asyncio
import logging
import os
import time
from contextlib import asynccontextmanager
from datetime import datetime
from functools import wraps

# Third-party package imports
import uvicorn # type: ignore
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Local imports
from model import LLMModel  # type: ignore
from database.database import DatabaseManager
from models.models import (
    ChatRequest,
    ChatResponse,
    ConversationRequest,
    ConversationResponse,
    GenerateRequest,
    GenerateResponse,
)

# TODO makefile for pylint and flake8
# TODO: Solid principles -> check about it.

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Default values for model parameters #TODO move it to config.py or .env file or .config file
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_LENGTH = 256

# Configure CORS
# Configure allowed origins based on environment
ALLOWED_ORIGINS = [
    "http://localhost:3000",  # Local development
    "https://your-frontend-domain.com",  # Production frontend
]


def validate_model(func):  # TODO move to utils.py or decorators.py
    """Decorator to validate that the LLM model is loaded before executing the endpoint"""

    @wraps(func)
    async def wrapper(*args, **kwargs):
        global llm_model
        if not llm_model or not llm_model.is_loaded():
            raise HTTPException(status_code=503, detail="Model not loaded")
        return await func(*args, **kwargs)

    return wrapper


def ensure_db(func):
    """Decorator to ensure database manager is available and inject it into the function"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        global db_manager

        if db_manager is None:
            # Try to reinitialize the database manager
            try:
                logger.warning("Database manager not initialized, attempting to reconnect...")
                db_manager = DatabaseManager()
                await db_manager.connect()
                logger.info("Database manager reconnected successfully")
            except Exception as e:
                logger.error(f"Failed to reinitialize database manager: {e}")
                raise HTTPException(
                    status_code=503,
                    detail="Database is not initialized. Please wait for the server to start up completely and try again.",
                )

        # Inject db_manager into function locals for the function to use
        func.__globals__['db'] = db_manager
        return await func(*args, **kwargs)

    return wrapper


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    """Initialize the LLM model and database on startup"""
    global llm_model, db_manager
    try:
        logger.info("Loading LLM model...")
        ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        llm_model = LLMModel(ollama_host=ollama_host)

        # Retry model loading with exponential backoff
        max_retries = 5
        for attempt in range(max_retries):
            try:
                await llm_model.load_model()
                logger.info("Model loaded successfully")
                break
            except Exception as e:
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt  # Exponential backoff: 1, 2, 4, 8, 16 seconds
                    logger.warning(f"Model loading attempt {attempt + 1} failed: {e}. Retrying in {wait_time} seconds...")
                    await asyncio.sleep(wait_time)
                else:
                    logger.error(f"Failed to load model after {max_retries} attempts: {e}")
                    raise

        # Initialize database - no need to pass host since it reads from env
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

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
@ensure_db
async def chat(request: ChatRequest):
    """Chat with the model using conversation history"""
    global llm_model  # TODO remove that
    # TODO : replace with single responsibility principle, and use a single function to handle each case (e.g., chat, generate, etc.)

    try:
        start_time = time.time()  # UTC time

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
            conversation_id = await db.create_conversation( # type: ignore
                user_id=request.user_id, title=f"Chat {len(request.messages)} messages"
            )
        else:
            # Verify the conversation exists if provided
            existing_conversation = await db.get_conversation(conversation_id) # type: ignore
            if not existing_conversation:
                raise HTTPException(
                    status_code=404,
                    detail=f"Conversation {conversation_id} not found"
                )


        # Save user messages to database
        for msg in request.messages:
            if msg.role == "user":
                await db.save_message( # type: ignore
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
        await db.save_message( # type: ignore
            conversation_id=conversation_id, role="assistant", content=response
        )

        # Save interaction statistics
        generation_time = int((time.time() - start_time) * 1000)
        await db.save_interaction_stats( # type: ignore
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
@ensure_db
async def create_conversation(request: ConversationRequest):
    try:
        conversation_id = await db.create_conversation( # type: ignore
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
@ensure_db
async def get_conversation_history(conversation_id: str, limit: int = 50):
    try:
        history = await db.get_conversation_history(conversation_id, limit) # type: ignore
        return {"conversation_id": conversation_id, "messages": history}
    except Exception as e:
        logger.error(f"Error getting conversation history: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get history: {str(e)}")


@app.get("/users/{user_id}/conversations")
@ensure_db
async def get_user_conversations(user_id: str, limit: int = 20):
    conversations = await db.get_user_conversations(user_id, limit) # type: ignore

    if not conversations:
        raise HTTPException(status_code=404, detail="No conversations found")

    return {"user_id": user_id, "conversations": conversations}


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
