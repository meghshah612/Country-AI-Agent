"""
Configuration module for Country Information AI Agent.
Handles environment variables and API configuration.
"""

import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuration class for managing application settings."""
    
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    REST_COUNTRIES_API_BASE_URL: str = "https://restcountries.com/v3.1"
    DEFAULT_MODEL: str = "gpt-4o-mini"
    MAX_RETRIES: int = 3
    REQUEST_TIMEOUT: int = 10
    
    @classmethod
    def validate(cls) -> None:
        """Validate that required configuration is present."""
        if not cls.OPENAI_API_KEY:
            raise ValueError(
                "OPENAI_API_KEY environment variable is not set. "
                "Please set it in your .env file or environment."
            )

