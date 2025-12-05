"""Configuration management for SQL Agent."""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings."""
    
    # Database configuration
    database_url: str = "sqlite:///./sales.db"
    
    # LLM configuration
    llm_provider: str = "openai"  # openai, anthropic, etc.
    openai_api_key: Optional[str] = None
    openai_base_url: Optional[str] = None  # For custom endpoints
    openai_model: str = "gpt-4o-mini"
    openai_temperature: float = 0.0
    
    # API configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    cors_origins: list[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    class Config:
        # Environment variables take precedence over .env file
        # In Docker, we rely on environment variables passed from docker-compose
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        # Pydantic Settings automatically reads from environment variables
        # Field names are converted: openai_api_key -> OPENAI_API_KEY


settings = Settings()

