"""
============================================================================
CONFIGURATION SETTINGS
============================================================================
Purpose: Centralized application configuration management
Usage: from config.settings import Settings
Interactions: Used by all modules to access configuration
Expansion: Add new settings as project grows
============================================================================
"""

# Standard Library Imports
import os
from pathlib import Path
from typing import Optional

# Third-Party Imports
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    """
    Application-wide configuration settings.
    
    This class provides centralized access to all configuration values,
    loaded from environment variables or using sensible defaults.
    
    Design Pattern: Singleton-like behavior (class attributes)
    Why: Ensures consistent configuration across the entire application
    
    Attributes:
        APP_NAME: Application name
        APP_VERSION: Current version
        ENVIRONMENT: dev/staging/production
        DEBUG: Enable debug mode
        BASE_DIR: Project root directory
        DATABASE_PATH: Path to SQLite database
        LOG_LEVEL: Logging verbosity
        LOG_FILE: Path to log file
        SESSION_TIMEOUT: Session expiration time (seconds)
        MAX_HISTORY_LENGTH: Maximum chat history to retain
    """
    
    # -------------------------------------------------------------------------
    # APPLICATION SETTINGS
    # -------------------------------------------------------------------------
    APP_NAME: str = os.getenv("APP_NAME", "Mini AI Chatbox")
    APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    # -------------------------------------------------------------------------
    # DIRECTORY PATHS
    # -------------------------------------------------------------------------
    # Get the project root directory (parent of config/)
    BASE_DIR: Path = Path(__file__).parent.parent
    
    # Database directory
    DATABASE_DIR: Path = BASE_DIR / "database"
    DATABASE_PATH: str = str(DATABASE_DIR / "chatbot.db")
    
    # Logs directory
    LOGS_DIR: Path = BASE_DIR / "logs"
    LOG_FILE: str = str(LOGS_DIR / "chatbot.log")
    
    # Data directories
    DATA_DIR: Path = BASE_DIR / "data"
    UPLOADS_DIR: Path = DATA_DIR / "uploads"
    EXPORTS_DIR: Path = DATA_DIR / "exports"
    TEMP_DIR: Path = DATA_DIR / "temp"
    
    # -------------------------------------------------------------------------
    # LOGGING CONFIGURATION
    # -------------------------------------------------------------------------
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # -------------------------------------------------------------------------
    # SESSION CONFIGURATION
    # -------------------------------------------------------------------------
    SESSION_TIMEOUT: int = int(os.getenv("SESSION_TIMEOUT", "3600"))
    MAX_HISTORY_LENGTH: int = int(os.getenv("MAX_HISTORY_LENGTH", "100"))
    
    # -------------------------------------------------------------------------
    # FILE UPLOAD SETTINGS
    # -------------------------------------------------------------------------
    MAX_UPLOAD_SIZE_MB: int = int(os.getenv("MAX_UPLOAD_SIZE_MB", "10"))
    ALLOWED_FILE_TYPES: list = os.getenv(
        "ALLOWED_FILE_TYPES", 
        "csv,xlsx,pdf,txt"
    ).split(",")
    
    # -------------------------------------------------------------------------
    # API KEYS (for future integrations)
    # -------------------------------------------------------------------------
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    GOOGLE_API_KEY: Optional[str] = os.getenv("GOOGLE_API_KEY")
    
    # -------------------------------------------------------------------------
    # STREAMLIT CONFIGURATION
    # -------------------------------------------------------------------------
    STREAMLIT_PORT: int = int(os.getenv("STREAMLIT_PORT", "8501"))
    STREAMLIT_THEME: str = os.getenv("STREAMLIT_THEME", "light")
    
    @classmethod
    def ensure_directories(cls) -> None:
        """
        Create necessary directories if they don't exist.
        
        Why: Prevents errors when trying to write to non-existent directories
        When to call: At application startup
        
        Future expansion: Add directory permissions validation
        """
        directories = [
            cls.DATABASE_DIR,
            cls.LOGS_DIR,
            cls.DATA_DIR,
            cls.UPLOADS_DIR,
            cls.EXPORTS_DIR,
            cls.TEMP_DIR,
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    @classmethod
    def is_production(cls) -> bool:
        """Check if running in production environment."""
        return cls.ENVIRONMENT.lower() == "production"
    
    @classmethod
    def is_development(cls) -> bool:
        """Check if running in development environment."""
        return cls.ENVIRONMENT.lower() == "development"
    
    @classmethod
    def get_database_url(cls) -> str:
        """
        Get database connection URL.
        
        Returns:
            SQLite connection string
            
        Future expansion: Support PostgreSQL/MySQL URLs
        """
        return f"sqlite:///{cls.DATABASE_PATH}"
    
    @classmethod
    def validate(cls) -> bool:
        """
        Validate that all required settings are properly configured.
        
        Returns:
            True if configuration is valid, False otherwise
            
        Raises:
            ValueError: If critical settings are missing
            
        TODO: Add validation for API keys when implementing AI features
        """
        # Check if critical paths exist
        if not cls.BASE_DIR.exists():
            raise ValueError(f"Base directory not found: {cls.BASE_DIR}")
        
        # Validate log level
        valid_log_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if cls.LOG_LEVEL.upper() not in valid_log_levels:
            raise ValueError(
                f"Invalid LOG_LEVEL: {cls.LOG_LEVEL}. "
                f"Must be one of: {valid_log_levels}"
            )
        
        return True
    
    @classmethod
    def display_config(cls) -> dict:
        """
        Get displayable configuration (excludes sensitive data).
        
        Returns:
            Dictionary of non-sensitive configuration values
            
        Why: Useful for debugging and logging startup configuration
        """
        return {
            "app_name": cls.APP_NAME,
            "version": cls.APP_VERSION,
            "environment": cls.ENVIRONMENT,
            "debug": cls.DEBUG,
            "log_level": cls.LOG_LEVEL,
            "database_path": cls.DATABASE_PATH,
            "session_timeout": cls.SESSION_TIMEOUT,
        }


# Initialize directories when module is imported
Settings.ensure_directories()


# Convenience function for getting settings
def get_settings() -> Settings:
    """
    Get application settings instance.
    
    Returns:
        Settings class with all configuration
        
    Usage:
        from config.settings import get_settings
        settings = get_settings()
        print(settings.APP_NAME)
    """
    return Settings
