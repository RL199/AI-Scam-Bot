from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from models.models import GenerateResponse, GenerateRequest, ChatResponse, ChatRequest
import uvicorn
import logging

from model import LLMModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="AI Scam Bot API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global model instance
llm_model = None


@app.on_event("startup")
async def startup_event():
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


@app.on_event("shutdown") #TODO "on_event" in class "FastAPI" is deprecated 
async def shutdown_event():
    """Cleanup on shutdown"""
    global llm_model
    if llm_model:
        await llm_model.cleanup()


@app.get("/")
async def root():
    return {"message": "AI Scam Bot API is running", "status": "healthy"}


@app.get("/health")
async def health_check():
    """Detailed health check"""
    global llm_model
    try:
        if llm_model and llm_model.is_loaded():
            return {"status": "healthy", "model_status": "loaded", "api_version": "1.0.0"}
        raise HTTPException(status_code=503, detail="Model not loaded")
    except HTTPException as error:
        raise error

@app.post("/generate", response_model=GenerateResponse)
async def generate_text(request: GenerateRequest):
    """Generate text from a prompt"""
    global llm_model

    if not llm_model or not llm_model.is_loaded():
        raise HTTPException(status_code=503, detail="Model not loaded")

    try:
        generated_text = await llm_model.generate(
            prompt=request.prompt,
            temperature=request.temperature or 0.7,
            top_p=request.top_p or 0.9,
        )

        return GenerateResponse(generated_text=generated_text, prompt=request.prompt)
    except Exception as e:
        logger.error(f"Generation error: {e}")
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest): #TODO  chat vs generate? why we have both? 
    # TODO NOTE: where is the conversation history stored? How do we manage it? Do we need to have another function to manage conversation history?
    """Chat with the model using conversation history"""
    global llm_model

    if not llm_model or not llm_model.is_loaded(): #TODO create a validate function instead of checking llm_model each time, you can include that on the model class or as a function\decorator
        raise HTTPException(status_code=503, detail="Model not loaded")

    try:
        # Convert ChatMessage objects to dictionaries
        messages_dict = [
            {"role": msg.role, "content": msg.content} for msg in request.messages
        ]

        response = await llm_model.chat(
            messages=messages_dict,
            max_length=request.max_length or 256,
            temperature=request.temperature or 0.7,
        )

        return ChatResponse(response=response)
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=f"Chat failed: {str(e)}")


@app.get("/model/info")
async def model_info():
    """Get information about the loaded model"""
    global llm_model

    if not llm_model:
        raise HTTPException(status_code=503, detail="Model not loaded")

    return await llm_model.get_model_info()


if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
