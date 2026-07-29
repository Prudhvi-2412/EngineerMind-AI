import os
from typing import List, Optional
from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "EngineeringOS AI Auth Service"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = False

    # Security & JWT
    JWT_SECRET_KEY: str = "SUPER_SECRET_CHANGE_ME_IN_PRODUCTION_0987654321"
    JWT_REFRESH_SECRET_KEY: str = "SUPER_SECRET_REFRESH_CHANGE_ME_IN_PRODUCTION_1234567890"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]

    # Database Settings
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "engineering_os_auth"
    DATABASE_URL: Optional[str] = None

    @field_validator("DATABASE_URL", mode="before")
    def assemble_db_connection(cls, v: Optional[str], values) -> str:
        if isinstance(v, str) and v:
            return v
        server = values.data.get("POSTGRES_SERVER", "localhost")
        port = values.data.get("POSTGRES_PORT", 5432)
        user = values.data.get("POSTGRES_USER", "postgres")
        password = values.data.get("POSTGRES_PASSWORD", "postgres")
        db = values.data.get("POSTGRES_DB", "engineering_os_auth")
        return f"postgresql+asyncpg://{user}:{password}@{server}:{port}/{db}"

    # Redis Settings
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_URL: Optional[str] = None

    @field_validator("REDIS_URL", mode="before")
    def assemble_redis_connection(cls, v: Optional[str], values) -> str:
        if isinstance(v, str) and v:
            return v
        host = values.data.get("REDIS_HOST", "localhost")
        port = values.data.get("REDIS_PORT", 6379)
        return f"redis://{host}:{port}/0"

    # Neo4j Graph Settings
    NEO4J_URI: str = "bolt://localhost:7687"
    NEO4J_USER: str = "neo4j"
    NEO4J_PASSWORD: str = "password123"

    # OpenAI AI Agent Settings
    OPENAI_API_KEY: str = "sk-placeholder_openai_api_key_12345"
    OPENAI_MODEL: str = "gpt-4o"

    # GitHub App & OAuth Configuration
    GITHUB_CLIENT_ID: str = "placeholder_github_client_id"
    GITHUB_CLIENT_SECRET: str = "placeholder_github_client_secret"
    GITHUB_REDIRECT_URI: str = "http://localhost:3000/oauth/callback?provider=github"
    GITHUB_APP_ID: str = "123456"
    GITHUB_APP_PRIVATE_KEY: str = ""
    GITHUB_WEBHOOK_SECRET: str = "super_secret_webhook_key_12345"

    # Google OAuth
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    GOOGLE_REDIRECT_URI: str = "http://localhost:8000/api/v1/auth/oauth/google/callback"

    # Microsoft OAuth
    MICROSOFT_CLIENT_ID: str = ""
    MICROSOFT_CLIENT_SECRET: str = ""
    MICROSOFT_TENANT_ID: str = "common"
    MICROSOFT_REDIRECT_URI: str = "http://localhost:8000/api/v1/auth/oauth/microsoft/callback"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )


settings = Settings()
