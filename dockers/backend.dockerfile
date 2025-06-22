FROM python:3.13-slim

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y curl && \
    curl -fsSL https://ollama.ai/install.sh | sh && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/. .

# Start Ollama service and pull model
RUN ollama serve & \
    sleep 10 && \
    ollama pull llama3.2-vision:11b

EXPOSE 8000

# Start both Ollama and FastAPI app
CMD ["sh", "-c", "ollama serve & uvicorn src.server:app --host 0.0.0.0 --port 8000"]
