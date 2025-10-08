"""
Configuration management for Silver Pancake backend.
Loads environment variables and provides application settings.

Interesting Fact: pydantic-settings automatically validates your config,
catching misconfiguration errors before they cause runtime issues!
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Azure OpenAI
    azure_openai_endpoint: str
    azure_openai_api_key: str
    azure_openai_deployment_name: str = "gpt-4"
    azure_openai_api_version: str = "2024-02-15-preview"
    
    # Azure Content Safety
    azure_content_safety_endpoint: str
    azure_content_safety_api_key: str
    
    # Application
    environment: str = "development"
    log_level: str = "INFO"
    cors_origins: str = "http://localhost:3000"
    
    # Optional: Application Insights
    applicationinsights_connection_string: str = ""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins from comma-separated string."""
        return [origin.strip() for origin in self.cors_origins.split(",")]


# Singleton instance
settings = Settings()
