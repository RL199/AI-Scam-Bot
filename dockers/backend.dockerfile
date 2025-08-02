FROM python:3.13-slim

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/. .

ENV PYTHONPATH=/app
# Configure service hosts for Docker network
ENV DATABASE_HOST=database
ENV OLLAMA_HOST=http://model:11434

EXPOSE 8000

# Start FastAPI app
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
