from functools import wraps
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from contextlib import asynccontextmanager

from models.models import GenerateResponse, GenerateRequest, ChatResponse, ChatRequest, ConversationRequest, ConversationResponse
import uvicorn
import logging
import time

from model import LLMModel
from database.database import DatabaseManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def validate_model(func):
    """Decorator to validate that the LLM model is loaded before executing the endpoint"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        global llm_model
        if not llm_model or not llm_model.is_loaded():
            raise HTTPException(status_code=503, detail="Model not loaded")
        return await func(*args, **kwargs)
    return wrapper

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
app.add_middleware( # TODO : limit access only to the docker's IP\ports to avoid security issues.
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global instances
llm_model = None
db_manager = None

@app.get("/")
async def root():
    return {"message": "AI Scam Bot API is running", "status": "healthy"}


@app.get("/health")
async def health_check():
    global llm_model
    try:
        if llm_model and llm_model.is_loaded():
            return {"status": "healthy", "model_status": "loaded", "api_version": "1.0.0"}
        raise HTTPException(status_code=503, detail="Model not loaded")
    except HTTPException as error:
        raise error


@app.post("/chat", response_model=ChatResponse)
@validate_model
async def chat(request: ChatRequest):
    """Chat with the model using conversation history"""
    global llm_model, db_manager

    try:
        start_time = time.time()

        # Create conversation if not provided
        conversation_id = request.conversation_id
        if not conversation_id:
            if db_manager is None:
                raise HTTPException(status_code=500, detail="Database manager not initialized")

            conversation_id = await db_manager.create_conversation(
                user_id=request.user_id,
                title=f"Chat {len(request.messages)} messages"
            )

        # Save user messages to database
        for msg in request.messages:
            if msg.role == "user":
                if db_manager is None:
                    raise HTTPException(status_code=500, detail="Database manager not initialized")
                await db_manager.save_message(
                    conversation_id=conversation_id,
                    role=msg.role,
                    content=msg.content
                )

        # Convert ChatMessage objects to dictionaries
        messages_dict = [
            {"role": msg.role, "content": msg.content} for msg in request.messages
        ]

        assert llm_model is not None
        response = await llm_model.chat(
            messages=messages_dict,
            max_length=256 if request.max_length is None else request.max_length,
            temperature=0.7 if request.temperature is None else request.temperature,
        )

        # Save assistant response to database
        if db_manager is None:
            raise HTTPException(status_code=500, detail="Database manager not initialized")
        await db_manager.save_message(
            conversation_id=conversation_id,
            role="assistant",
            content=response
        )

        # Save interaction statistics
        generation_time = int((time.time() - start_time) * 1000)
        if db_manager is None:
            raise HTTPException(status_code=500, detail="Database manager not initialized")
        await db_manager.save_interaction_stats(
            conversation_id=conversation_id,
            generation_time_ms=generation_time,
            model_name=llm_model.model_name,
            temperature=0.7 if request.temperature is None else request.temperature,
            max_length=256 if request.max_length is None else request.max_length
        )

        return ChatResponse(response=response, conversation_id=conversation_id)
    except Exception as error:
        logger.error(f"Chat error: {error}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Chat failed: {error}")


@app.post("/conversations", response_model=ConversationResponse)
async def create_conversation(request: ConversationRequest):
    """Create a new conversation"""
    global db_manager

    try:
        if db_manager is None:
            raise HTTPException(status_code=500, detail="Database manager not initialized")
        conversation_id = await db_manager.create_conversation(
            user_id=request.user_id,
            title=request.title
        )

        return ConversationResponse(
            conversation_id=conversation_id,
            title=request.title,
            created_at=str(time.time())
        )
    except Exception as e:
        logger.error(f"Error creating conversation: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create conversation: {str(e)}")


@app.get("/conversations/{conversation_id}/history")
async def get_conversation_history(conversation_id: str, limit: int = 50):
    """Get conversation history"""
    global db_manager

    try:
        if db_manager is None:
            raise HTTPException(status_code=500, detail="Database manager not initialized")
        history = await db_manager.get_conversation_history(conversation_id, limit)
        return {"conversation_id": conversation_id, "messages": history}
    except Exception as e:
        logger.error(f"Error getting conversation history: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get history: {str(e)}")


@app.get("/users/{user_id}/conversations")
async def get_user_conversations(user_id: str, limit: int = 20):
    """Get user's conversations"""
    global db_manager

    try:
        if db_manager is None:
            raise HTTPException(status_code=500, detail="Database manager not initialized")
        conversations = await db_manager.get_user_conversations(user_id, limit)
        return {"user_id": user_id, "conversations": conversations}
    except Exception as e:
        logger.error(f"Error getting user conversations: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get conversations: {str(e)}")

@app.get("/model/info")
@validate_model
async def model_info():
    """Get information about the loaded model"""
    global llm_model
    assert llm_model is not None
    return await llm_model.get_model_info()


if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
