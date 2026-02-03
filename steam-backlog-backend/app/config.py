from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    Create a .env file in the root directory with these values.
    """
    
    # Steam API
    steam_api_key: str
    steam_openid_url: str = "https://steamcommunity.com/openid/login"
    
    # URLs
    frontend_url: str = "http://localhost:3000"
    backend_url: str = "http://localhost:8000"
    
    # Database (optional - depends on if you use Supabase or PostgreSQL)
    database_url: Optional[str] = None
    supabase_url: Optional[str] = None
    supabase_key: Optional[str] = None
    
    # LLM API Keys (for AI recommendations)
    anthropic_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Create a global settings instance
settings = Settings()
