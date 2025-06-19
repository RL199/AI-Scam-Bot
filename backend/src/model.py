import torch
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
)
from transformers.generation.configuration_utils import GenerationConfig
from transformers.utils.quantization_config import BitsAndBytesConfig
import logging
from typing import List, Dict, Optional, Any
import asyncio
from threading import Thread
import gc
import os

logger = logging.getLogger(__name__)

class LLMModel:
    MAX_LENGTH = 256  # Default max length for generation
    def __init__(self, model_name: str = "microsoft/DialoGPT-medium"):
        self.model_name = model_name
        self.model = None
        self.tokenizer = None
        self.device = self._get_device()
        self.generation_config = None
        self._loaded = False

        # Configure for memory efficiency
        self.max_memory_gb = 4  # Adjust based on available RAM
        self.use_4bit = True if torch.cuda.is_available() else False

    def _get_device(self) -> str:
        """Determine the best device for the model"""
        if torch.cuda.is_available():
            return "cuda"
        elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
            return "mps"  # Apple Silicon
        else:
            return "cpu"

    async def load_model(self):
        """Load the model and tokenizer asynchronously"""
        try:
            logger.info(f"Loading model {self.model_name} on device: {self.device}")

            # Run model loading in a separate thread to avoid blocking
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, self._load_model_sync)

            self._loaded = True
            logger.info("Model loaded successfully")

        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise

    def _load_model_sync(self):
        """Synchronous model loading"""
        # Load tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_name,
            padding_side='left'
        )

        # Add pad token if it doesn't exist
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

        # Configure quantization for memory efficiency
        quantization_config = None
        if self.use_4bit and self.device == "cuda":
            quantization_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_compute_dtype=torch.float16,
                bnb_4bit_use_double_quant=True,
                bnb_4bit_quant_type="nf4"
            )

        # Load model with appropriate configuration
        model_kwargs = {
            "torch_dtype": torch.float16 if self.device != "cpu" else torch.float32,
            "low_cpu_mem_usage": True,
            "trust_remote_code": True
        }

        if quantization_config:
            model_kwargs["quantization_config"] = quantization_config
        else:
            model_kwargs["device_map"] = "auto" if self.device == "cuda" else None

        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            **model_kwargs
        )

        # Move to device if not using device_map
        if not quantization_config and self.device != "cuda":
            self.model = self.model.to(self.device)

        # Set generation config
        self.generation_config = GenerationConfig(
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
            top_k=50,
            repetition_penalty=1.1,
            length_penalty=1.0,
            max_new_tokens=256,
            pad_token_id=self.tokenizer.pad_token_id,
            eos_token_id=self.tokenizer.eos_token_id,
            use_cache=True
        )

        # Enable gradient checkpointing for memory efficiency
        if hasattr(self.model, 'gradient_checkpointing_enable'):
            self.model.gradient_checkpointing_enable()

    def is_loaded(self) -> bool:
        """Check if model is loaded"""
        return self._loaded and self.model is not None and self.tokenizer is not None

    async def generate(
        self,
        prompt: str,
        max_length: int = MAX_LENGTH,
        temperature: float = 0.7,
        top_p: float = 0.9
    ) -> str:
        """Generate text from a prompt"""
        if not self.is_loaded():
            raise RuntimeError("Model not loaded")

        try:
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None,
                self._generate_sync,
                prompt,
                max_length,
                temperature,
                top_p
            )
            return result
        except Exception as e:
            logger.error(f"Generation error: {e}")
            raise

    def _generate_sync(
        self,
        prompt: str,
        max_length: int,
        temperature: float,
        top_p: float
    ) -> str:
        """Synchronous text generation"""
        # Check if tokenizer and model are loaded
        if not self.model:
            raise RuntimeError("Model not initialized. Make sure to call load_model first and wait for it to complete.")

        if not self.tokenizer:
            raise RuntimeError("Tokenizer not initialized. Make sure to call load_model first.")

        # Encode input
        inputs = self.tokenizer.encode(
            prompt + self.tokenizer.eos_token,
            return_tensors='pt'
        ).to(self.device)

        # Update generation config
        if self.generation_config is None:
            # Create default config if none exists
            self.generation_config = GenerationConfig(
                do_sample=True,
                temperature=0.7,
                top_p=0.9,
                top_k=50,
                repetition_penalty=1.1,
                length_penalty=1.0,
                max_new_tokens=256,
                pad_token_id=self.tokenizer.pad_token_id,
                eos_token_id=self.tokenizer.eos_token_id,
                use_cache=True
            )

        gen_config = GenerationConfig(
            **self.generation_config.to_dict(),
            max_new_tokens=min(max_length, 512),
            temperature=temperature,
            top_p=top_p
        )

        # Generate
        with torch.no_grad():
            outputs = self.model.generate(
                inputs,
                generation_config=gen_config,
                pad_token_id=self.tokenizer.pad_token_id
            )

        # Decode response
        response = self.tokenizer.decode(
            outputs[0][inputs.shape[-1]:],
            skip_special_tokens=True
        )

        return response.strip()

    async def chat(
        self,
        messages: List[Dict[str, str]],
        max_length: int = 256,
        temperature: float = 0.7
    ) -> str:
        """Chat with conversation history"""
        if not self.is_loaded():
            raise RuntimeError("Model not loaded")

        try:
            # Convert messages to conversation format
            conversation = ""
            eos_token = self.tokenizer.eos_token if self.tokenizer else ""
            for msg in messages[-5:]:  # Keep last 5 messages for context
                role = msg.get("role", "user")
                content = msg.get("content", "")

                if role == "user":
                    conversation += f"User: {content}{eos_token}"
                elif role == "assistant":
                    conversation += f"Bot: {content}{eos_token}"

            conversation += "Bot:"

            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None,
                self._generate_sync,
                conversation,
                max_length,
                temperature,
                0.9
            )
            return result

        except Exception as e:
            logger.error(f"Chat error: {e}")
            raise

    async def get_model_info(self) -> Dict[str, Any]:
        """Get model information"""
        info = {
            "model_name": self.model_name,
            "device": self.device,
            "loaded": self.is_loaded(),
            "use_4bit": self.use_4bit,
            "torch_version": torch.__version__
        }

        if self.is_loaded():
            info.update({
                "vocab_size": self.tokenizer.vocab_size if self.tokenizer else 0,
                "model_type": self.model.config.model_type if self.model else "unknown",
                "num_parameters": sum(p.numel() for p in self.model.parameters()) if self.model else 0
            })

            # Memory info
            if torch.cuda.is_available():
                info["gpu_memory"] = {
                    "allocated": torch.cuda.memory_allocated(0) / 1024**3,
                    "cached": torch.cuda.memory_reserved(0) / 1024**3
                }

        return info

    async def cleanup(self):
        """Cleanup model resources"""
        try:
            if self.model is not None:
                del self.model
                self.model = None

            if self.tokenizer is not None:
                del self.tokenizer
                self.tokenizer = None

            # Clear GPU cache
            if torch.cuda.is_available():
                torch.cuda.empty_cache()

            # Force garbage collection
            gc.collect()

            self._loaded = False
            logger.info("Model cleanup completed")

        except Exception as e:
            logger.error(f"Cleanup error: {e}")

    def __del__(self):
        """Destructor to ensure cleanup"""
        if self._loaded:
            try:
                asyncio.create_task(self.cleanup())
            except:
                pass  # Best effort cleanup
