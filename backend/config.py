"""
Configuration management for Hybrid-Analyzer backend.
Loads environment variables and provides centralized settings.
"""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Database
    database_url: str = "postgresql://postgres:postgres@localhost:5432/hybrid_analyzer"
    
    # JWT Authentication
    jwt_secret: str = "your-secret-key-change-this-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expiration_minutes: int = 60 * 24  # 24 hours
    
    # API Keys
    huggingface_api_token: str = ""
    gemini_api_key: str = ""
    
    # CORS
    cors_origins: list = ["http://localhost:3000", "http://localhost:5173"]
    
    # API Configuration
    huggingface_model: str = "facebook/bart-large-mnli"
    huggingface_api_url: str = "https://api-inference.huggingface.co/models"
    
    # Timeouts (seconds)
    huggingface_timeout: int = 60
    gemini_timeout: int = 60
    
    # Logging
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance with Vercel fixes."""
    settings = Settings()
    
    # Vercel/Neon often provides POSTGRES_URL instead of DATABASE_URL
    import os
    if not settings.database_url or "localhost" in settings.database_url:
        if os.getenv("POSTGRES_URL"):
            settings.database_url = os.getenv("POSTGRES_URL")
    
    # SQLAlchemy requires 'postgresql://', but some providers give 'postgres://'
    if settings.database_url and settings.database_url.startswith("postgres://"):
        settings.database_url = settings.database_url.replace("postgres://", "postgresql://", 1)
        
    return settings
