import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    """Application settings"""
    
    # API Keys
    anthropic_api_key: Optional[str] = Field(None, env="ANTHROPIC_API_KEY")
    openai_api_key: Optional[str] = Field(None, env="OPENAI_API_KEY")
    app_secret_key: Optional[str] = Field(None, env="APP_SECRET_KEY")
    
    # App Settings
    debug: bool = Field(False, env="DEBUG")
    host: str = Field("127.0.0.1", env="HOST")
    port: int = Field(8050, env="PORT")
    
    # UI Settings
    app_title: str = "Data Science Assistant"
    theme: str = "BOOTSTRAP"  # Can be CYBORG, DARKLY, etc.
    
    # Tool Settings
    max_file_size_mb: int = 100
    max_plots_history: int = 20
    
    # Performance
    update_interval_ms: int = 100
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"  # Allow extra fields in .env file

# Create global config instance
AppConfig = Settings()