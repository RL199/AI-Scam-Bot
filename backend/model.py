# Python standard library imports
import asyncio
import logging
from typing import List, Dict, Any, Optional

# Third-party package imports
import ollama

# Local imports
# (none in this file)

class LLMModel:

    def __init__(
        self,
        model_name: str = "ITModel",
        logger: logging.Logger = logging.getLogger(__name__),
        ollama_host: str = "http://localhost:11434",
    ) -> None:
        self.logger = logger
        self.model_name = model_name
        self.client: Optional[ollama.AsyncClient] = None
        self._loaded = False
        self.ollama_host = ollama_host

    async def load_model(self) -> None:
        """Initialize Ollama client and verify model availability"""
        try:
            self.logger.info(f"Initializing Ollama client for model: {self.model_name}")

            # Initialize Ollama client
            self.client = ollama.AsyncClient(host=self.ollama_host)

            # Check if model is available locally
            await self._ensure_model_available()

            self._loaded = True
            self.logger.info("Ollama model initialized successfully")

        except Exception as e:
            self.logger.error(f"Failed to initialize Ollama model: {e}")
            raise

    async def _ensure_model_available(self) -> None:
        """Ensure the model is downloaded and available"""
        if self.client is None:
            raise RuntimeError("Client not initialized")

        try:
            # List available models
            models = await self.client.list()
            model_names = [
                model.get("name")
                for model in models.get("models", [])
                if model.get("name")
            ]
            if self.model_name not in model_names:
                self.logger.info(
                    f"Model {self.model_name} not found locally. Checking if it's a custom model..."
                )

                # For custom models like ITModel, we need to wait for them to be created
                # rather than trying to pull them
                if self.model_name == "ITModel":
                    self.logger.info(
                        f"Custom model {self.model_name} not found. It should be created by the model service."
                    )
                    # Don't try to pull custom models - they should be created by the model service
                    return
                else:
                    # Pull the model if it's a standard model
                    self.logger.info(
                        f"Model {self.model_name} not found locally. Downloading..."
                    )
                    await self.client.pull(self.model_name)
                    self.logger.info(f"Model {self.model_name} downloaded successfully")
            else:
                self.logger.info(f"Model {self.model_name} is available locally")

        except Exception as e:
            self.logger.error(f"Error checking/downloading model: {e}")
            raise

    def is_loaded(self) -> bool:
        return self._loaded and self.client is not None

    async def generate(
        self,
        prompt: str,
    ) -> str:
        """Generate text from a prompt using Ollama"""
        if not self.is_loaded():
            raise RuntimeError("Model not loaded")

        if self.client is None:
            raise RuntimeError("Client not initialized")

        try:
            response = await self.client.generate(
                model=self.model_name,
                prompt=prompt,
            )

            return response["response"].strip()

        except Exception as e:
            self.logger.error(f"Generation error: {e}")
            raise

    async def chat(
        self,
        messages: List[Dict[str, str]],
    ) -> str:
        """Chat with conversation history using Ollama's chat API"""
        if not self.is_loaded():
            raise RuntimeError("Model not loaded")

        try:
            # Convert messages to Ollama format
            ollama_messages = []
            for msg in messages[-10:]:  # Keep last 10 messages for context
                role = msg.get("role", "user")
                content = msg.get("content", "")

                # Ensure role is valid (default to "user" if not recognized)
                if role not in ["assistant", "system", "user"]:
                    role = "user"

                ollama_messages.append({"role": role, "content": content})

            if self.client is None:
                raise RuntimeError("Client not initialized")

            response = await self.client.chat(
                model=self.model_name,
                messages=ollama_messages,
            )

            return response["message"]["content"].strip()

        except Exception as e:
            self.logger.error(f"Chat error: {e}")
            raise

    async def get_model_info(self) -> Dict[str, Any]:
        """Get model information from Ollama"""
        info = {
            "model_name": self.model_name,
            "loaded": self.is_loaded(),
            "ollama_host": self.ollama_host,
            "backend": "ollama",
        }

        if self.is_loaded() and self.client is not None:
            try:
                # Get model details from Ollama
                model_info = await self.client.show(self.model_name)
                info.update(
                    {
                        "model_info": model_info.get("details", {}),
                        "parameters": model_info.get("parameters", {}),
                        "template": model_info.get("template", "Unknown"),
                        "family": model_info.get("details", {}).get(
                            "family", "Unknown"
                        ),
                        "format": model_info.get("details", {}).get(
                            "format", "Unknown"
                        ),
                        "size": model_info.get("size", 0),
                    }
                )
            except Exception as e:
                self.logger.error(f"Error getting model info: {e}")
                info["error"] = str(e)

        return info

    async def cleanup(self) -> None:
        """Cleanup Ollama client resources"""
        try:
            if self.client:
                # Ollama client doesn't require explicit cleanup
                # but we can close the connection if needed
                self.client = None

            self._loaded = False
            self.logger.info("Ollama model cleanup completed")

        except Exception as e:
            self.logger.error(f"Cleanup error: {e}")

    def __del__(self) -> None:
        """Destructor to ensure cleanup"""
        if self._loaded:
            try:
                asyncio.create_task(self.cleanup())
            except:
                pass  # Best effort cleanup
