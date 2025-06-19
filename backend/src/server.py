from functools import wraps
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from contextlib import asynccontextmanager

from models.models import GenerateResponse, GenerateRequest, ChatResponse, ChatRequest
import uvicorn
import logging

from model import LLMModel

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
    """Initialize the LLM model on startup"""
    global llm_model
    try:
        logger.info("Loading LLM model...")
        llm_model = LLMModel()
        await llm_model.load_model() # TODO: NOTE: what will happen if the model takes too long to load? Should we have a timeout or a background task?
        logger.info("Model loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        raise # TODO: NOTE: How to handle a model failure? shoud we cretae some retry logic or a fallback mechanism? Or just raise an error and stop the server?

    yield

    if llm_model:
        await llm_model.cleanup()


app = FastAPI(title="AI Scam Bot API", version="1.0.0", lifespan=lifespan)

# Configure CORS
app.add_middleware( # TODO : limit access only to the docker's IP\ports to avoid security issues.
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global model instance
llm_model = None

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
    global llm_model

    try:
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

        return ChatResponse(response=response)
    except Exception as error:
        logger.error(f"Chat error: {error}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Chat failed: {error}")


@app.get("/model/info")
@validate_model
async def model_info():
    """Get information about the loaded model"""
    global llm_model
    assert llm_model is not None
    return await llm_model.get_model_info()


if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
