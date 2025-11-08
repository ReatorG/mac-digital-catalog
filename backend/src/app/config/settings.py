from pydantic_settings import BaseSettings
from pydantic import Field, field_validator
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent  # now points to mac/
ENV_FILE = BASE_DIR / ".env"

class Settings(BaseSettings):
    # ================================
    # Database
    # ================================
    DATABASE_URL: str

    POSTGRES_HOST: str
    POSTGRES_PORT: int = Field(default=5432)
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    # ================================
    # App Configuration
    # ================================
    APP_ENV: str = Field(default="development")
    DEBUG: bool = Field(default=True)
    API_HOST: str = Field(default="0.0.0.0")
    API_PORT: int = Field(default=8000)

    # ================================
    # CORS
    # ================================
    ALLOWED_ORIGINS: list[str] = Field(default=["http://localhost:3000"])

    # ================================
    # Validators
    # ================================
    @field_validator('POSTGRES_PORT', 'API_PORT', mode='before')
    @classmethod
    def validate_ports(cls, v: Any) -> int:
        if v in ('', None):
            return 5432
        try:
            return int(v)
        except ValueError:
            return 5432

    @field_validator('DEBUG', mode='before')
    @classmethod
    def validate_debug(cls, v: Any) -> bool:
        if isinstance(v, str):
            return v.lower() in ('true', '1', 'yes', 'on')
        return bool(v)

print("=== DEBUG SETTINGS PATHS ===")
print("File:", __file__)
print("Base dir:", BASE_DIR)
print("Env file absolute path:", ENV_FILE)
print("Exists:", ENV_FILE.exists())
print("=============================")


# Instantiate global settings object
settings = Settings(_env_file=ENV_FILE)
