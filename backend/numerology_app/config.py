"""
Configuration module for the numerology application.

This module provides configuration settings for the panchangam engine
and other application components.
"""

from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Default timezone
    DEFAULT_TZ: str = "Asia/Kolkata"
    
    # Redis configuration
    REDIS_URL: Optional[str] = None
    
    # Database configuration
    DATABASE_URL: Optional[str] = None
    
    # Panchangam configuration
    AYANAMSA: str = "Lahiri"  # Default ayanamsa system
    MONTH_SYSTEM: str = "Amanta"  # Amanta or Purnimanta
    DAY_BOUNDARY: str = "sunrise"  # sunrise or sunset
    
    # API configuration
    API_V1_STR: str = "/api"
    PROJECT_NAME: str = "Astrooverz Numerology API"
    
    # CORS settings
    BACKEND_CORS_ORIGINS: list[str] = ["*"]
    
    # Job scheduling configuration
    SCHED_ENABLED: bool = False
    CITY_PRECOMPUTE: str = "IN_TOP200"  # IN_TOP200, IN_TOP50, IN_TOP10, ALL
    PRECOMPUTE_DAYS: int = 30  # Number of days to precompute
    PRECOMPUTE_TIME: str = "02:30"  # Time to run precompute job (IST)

    model_config = {"env_file": ".env", "extra": "ignore"}

# Global settings instance
settings = Settings()
