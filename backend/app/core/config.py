from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ROOT_DIR / '.env', env_file_encoding='utf-8', extra='ignore')

    app_env: Literal['development', 'test', 'production'] = 'development'
    database_url: SecretStr = SecretStr('postgresql+psycopg://puppletrouble:change-local-db-password@127.0.0.1:5678/puppletrouble')
    jwt_secret: SecretStr = SecretStr('')
    model_api_key: SecretStr = SecretStr('')
    model_api_base_url: str = ''
    model_name: str = ''
    ai_mode: Literal['real', 'mock'] = 'mock'
    storage_dir: Path = Path('storage')
    max_upload_mb: int = 10
    max_image_pixels: int = 25_000_000
    allow_dev_http: bool = True
    cors_origins: str = 'http://localhost:5173,http://127.0.0.1:5173,http://localhost:4173,http://127.0.0.1:4173'

    @property
    def allowed_origins(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(',') if origin.strip()]

    @property
    def storage_path(self) -> Path:
        return self.storage_dir if self.storage_dir.is_absolute() else ROOT_DIR / self.storage_dir

    @model_validator(mode='after')
    def validate_production(self):
        if self.app_env == 'production':
            if self.ai_mode == 'mock' or self.allow_dev_http:
                raise ValueError('生产环境必须关闭模拟模式和开发 HTTP')
            secret = self.jwt_secret.get_secret_value()
            if len(secret) < 32 or secret.startswith('replace-'):
                raise ValueError('生产环境需要有效的 JWT_SECRET')
        return self


@lru_cache
def get_settings() -> Settings:
    return Settings()
