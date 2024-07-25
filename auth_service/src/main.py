from contextlib import asynccontextmanager
import logging

from api import not_auth_router, auth_router, admin_router
from core.exception import global_exception_handler
from core.config import settings
from db import redis
from db.postgres import engine
from fastapi.responses import ORJSONResponse
from redis.asyncio import Redis

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

logger = logging.getLogger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    engine.connect()
    yield
    engine.dispose()


app = FastAPI(
    # Конфигурируем название проекта.
    title=settings.project_name,
    # Описание проекта.
    description="Это API для регистрации и аутентификации пользователей с использованием токенов JWT.",
    # Адрес документации в красивом интерфейсе
    docs_url="/auth/openapi",
    # Адрес документации в формате OpenAPI
    openapi_url="/auth/openapi.json",
    # Можно сразу сделать небольшую оптимизацию сервиса
    # и заменить стандартный JSON-сериализатор на более шуструю версию, написанную на Rust
    default_response_class=ORJSONResponse,
    exception_handlers={Exception: global_exception_handler}
)


@app.router.on_startup.append
async def startup():
    redis.redis = Redis(host=settings.redis_host, port=settings.redis_port)


@app.router.on_shutdown.append
async def shutdown():
    await redis.redis.close()

origins = settings.origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(not_auth_router)
app.include_router(auth_router)
app.include_router(admin_router)
