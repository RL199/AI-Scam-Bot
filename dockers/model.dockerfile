FROM ollama/ollama:0.9.5

# Install curl for health checks
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY model/requirements.txt .

COPY model/. .

COPY backend/models/Modelfile ./Modelfile

EXPOSE 11434

# Start Ollama service
ENTRYPOINT ["/bin/bash", "-c"]
CMD ["ollama serve & sleep 10 && ollama pull llama3.2:3b && ollama create ITModel -f ./Modelfile && echo 'ITModel created successfully' && tail -f /dev/null"]
