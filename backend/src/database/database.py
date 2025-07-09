# Python standard library imports
import json
import logging
import uuid
from contextlib import asynccontextmanager
from datetime import datetime
from functools import wraps
from typing import Optional, List, Dict, Any

# Third-party package imports
import aiomysql

# Local imports
# (none in this file)


logger = logging.getLogger(__name__)

# Constants
VALID_MESSAGE_ROLES = ["user", "assistant", "system"]


def ensure_pool_initialized(func):
    """Decorator to check if database pool is initialized before method execution"""

    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        if self.pool is None:
            raise RuntimeError("Database connection pool is not initialized")
        return await func(self, *args, **kwargs)

    return wrapper

class DatabaseManager:
    def __init__(
        self,
        host: str = "localhost",
        port: int = 3306,
        user: str = "scambot_user",
        password: str = "scambot_password",
        database: str = "scambot_db",
    ):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.pool = None

    async def connect(self):
        """Initialize database connection pool"""
        try:
            self.pool = await aiomysql.create_pool(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                db=self.database,
                autocommit=False,
                minsize=1,
                maxsize=10,
            )
            logger.info("Database connection pool created successfully")
        except aiomysql.Error as error:
            logger.error(f"Error creating database connection pool: {error}")
            raise RuntimeError(f"Failed to connect to database: {error}")

    async def disconnect(self):
        """Close database connection pool"""
        if self.pool:
            self.pool.close()
            await self.pool.wait_closed()
            logger.info("Database connection pool closed")

    @ensure_pool_initialized
    async def create_conversation(
        self, user_id: Optional[str] = None, title: Optional[str] = None
    ) -> str:
        """Create a new conversation and return its ID"""
        conversation_id = str(uuid.uuid4())

        try:
            async with self.pool.acquire() as conn: # type: ignore
                async with conn.cursor() as cursor:
                    await cursor.execute(
                        "INSERT INTO conversations (id, user_id, title) VALUES (%s, %s, %s)",
                        (conversation_id, user_id, title),
                    )
                    await conn.commit()

            logger.info(f"Created new conversation: {conversation_id}")
            return conversation_id

        except aiomysql.Error as error:
            logger.error(f"Database error creating conversation {conversation_id}: {error}")
            raise RuntimeError(f"Failed to create conversation: {error}")
        except Exception as error:
            logger.error(f"Unexpected error creating conversation {conversation_id}: {error}")
            raise RuntimeError(f"Unexpected error creating conversation: {error}")

    @ensure_pool_initialized
    async def save_message(
        self,
        conversation_id: str,
        role: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        """Save a message to the database"""

        if role not in VALID_MESSAGE_ROLES:
            raise ValueError(
                f"Invalid role: {role}. Must be one of: {', '.join(VALID_MESSAGE_ROLES)}"
            )

        async with self.pool.acquire() as conn: # type: ignore
            async with conn.cursor() as cursor:
                await cursor.execute(
                    "INSERT INTO messages (conversation_id, role, content, metadata) VALUES (%s, %s, %s, %s)",
                    (
                        conversation_id,
                        role,
                        content,
                        json.dumps(metadata) if metadata else None,
                    ),
                )

    @ensure_pool_initialized
    async def save_interaction_stats(
        self,
        conversation_id: str,
        generation_time_ms: int,
        model_name: str,
        temperature: float,
        max_length: int,
        prompt_tokens: int = 0,
        response_tokens: int = 0,
    ):
        """Save interaction statistics"""

        try:
            async with self.pool.acquire() as conn: # type: ignore
                async with conn.cursor() as cursor:
                    await cursor.execute(
                        """INSERT INTO interaction_stats
                        (conversation_id, generation_time_ms, model_name, temperature, max_length,
                            prompt_tokens, response_tokens)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                        (
                            conversation_id,
                            generation_time_ms,
                            model_name,
                            temperature,
                            max_length,
                            prompt_tokens,
                            response_tokens,
                        ),
                    )
                    await conn.commit()

            logger.info(f"Saved interaction stats for conversation: {conversation_id}")

        except aiomysql.Error as error:
            logger.error(f"Database error saving interaction stats for conversation {conversation_id}: {error}")
            raise RuntimeError(f"Failed to save interaction stats: {error}")
        except Exception as error:
            logger.error(f"Unexpected error saving interaction stats for conversation {conversation_id}: {error}")
            raise RuntimeError(f"Unexpected error saving interaction stats: {error}")

    @ensure_pool_initialized
    async def get_conversation_history(
        self, conversation_id: str, limit: int = 50
    ) -> List[Dict[str, Any]]:
        """Get conversation history"""

        async with self.pool.acquire() as conn: # type: ignore
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(
                    """SELECT role, content, timestamp, metadata
                       FROM messages
                       WHERE conversation_id = %s
                       ORDER BY timestamp ASC
                       LIMIT %s""",
                    (conversation_id, limit),
                )
                return await cursor.fetchall()

    @ensure_pool_initialized
    async def get_user_conversations(
        self, user_id: str, limit: int = 20
    ) -> List[Dict[str, Any]]:
        """Get user's conversations"""

        async with self.pool.acquire() as conn: # type: ignore
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(
                    """SELECT id, title, created_at, updated_at
                       FROM conversations
                       WHERE user_id = %s
                       ORDER BY updated_at DESC
                       LIMIT %s""",
                    (user_id, limit),
                )
                return await cursor.fetchall()
