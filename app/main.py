import logging
from fastapi import FastAPI

from app.api.routes import base_controller
from app.database.models.base import Base
from app.database.database import engine
from app.api.dependencies import auth

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s | %(asctime)s | %(name)s |  %(message)s",
    handlers=[
        logging.FileHandler("app/core/app.log"),
        logging.StreamHandler()
    ]
)

app = FastAPI()

app.include_router(
    auth.router,
    tags=['auth']
)

app.include_router(
    base_controller.router,
    prefix='/api/v1'
)


@app.on_event("startup")
async def startup():
    # Используем соединение напрямую для выполнения синхронной операции
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown():
    # Закрываем соединение с базой данных при завершении работы
    await engine.dispose()