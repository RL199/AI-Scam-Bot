FROM ollama/ollama:0.9.5

# Install envsubst for environment variable substitution
RUN apt-get update && apt-get install -y gettext-base && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY model/requirements.txt .

COPY model/. .

COPY backend/models/Modelfile ./Modelfile

EXPOSE 11434

# Start Ollama service
ENTRYPOINT ["/bin/bash", "-c"]
CMD ["ollama serve & sleep 10 && ollama pull ${OLLAMA_MODEL:-llama3.2-vision:11b} && envsubst < ./Modelfile > ./Modelfile.tmp && mv ./Modelfile.tmp ./Modelfile && ollama create ITModel -f ./Modelfile && echo 'ITModel created successfully' && tail -f /dev/null"]
