from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    # Название проекта
    project_name: str = Field("Сервис авторизации", env="PROJECT_NAME")

    # Настройка БД
    db_host: str = Field("127.0.0.1", env="DB_HOST")
    db_port: str = Field("5432", env="DB_PORT")
    db_name: str = Field("movies_auth", env="DB_NAME")
    db_user: str = Field("auth", env="DB_USER")
    db_password: str = Field("123qwe", env="DB_PASSWORD")

    # Настройки Redis
    redis_host: str = Field("127.0.0.1", env="REDIS_HOST")
    redis_port: int = Field(6379, env="REDIS_PORT")

    # Корень проекта
    base_dir: str = Field("/src", env="BASE_DIR")

    # Соль
    salt: str = Field("$2b$12$IvGyiwB/y/SIdpGk2xp.BO", env="SALT")

    # Время жизни токенов
    life_access_token: int = Field(60 * 60 * 3, env="LIFE_ACCESS_TOKEN")
    life_refresh_token: int = Field(60 * 60 * 24 * 7, env="LIFE_REFRESH_TOKEN")

    # Добавьте все необходимые домены
    origins: list = Field([
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "http://www.example.com"
        ], env="ORIGINS")

    postgres_indexes_naming_convention: dict = {
        "ix": "%(column_0_label)s_idx",
        "uq": "%(table_name)s_%(column_0_name)s_key",
        "ck": "%(table_name)s_%(constraint_name)s_check",
        "fk": "%(table_name)s_%(column_0_name)s_fkey",
        "pk": "%(table_name)s_pkey",
    }

    # username и пароль для суперюзера
    superuser_username: str = Field("superadmin")
    superuser_password: str = Field("password")
    superuser_email: str = Field("admin@example.com")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @property
    def database_url(self) -> str:
        return f'postgresql+psycopg2://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}'

    @property
    def database_async_url(self) -> str:
        return f'postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}'


@lru_cache
def get_config() -> Settings:
    return Settings()


settings = get_config()
