FROM ollama/ollama:0.9.5

WORKDIR /app

COPY model/requirements.txt .

COPY model/. .

EXPOSE 11434

# Start Ollama service
ENTRYPOINT ["/bin/bash", "-c"]
CMD ["ollama serve & sleep 5 && ollama pull llama3.2:3b && tail -f /dev/null"]
