import logging
from fastapi import FastAPI

from app.core.logger import setup_logging
from app.core.config import ALLOWED_HOSTS
from app.middlewares.cors import setup_cors
from app.api.routes import route, auth_controller
from app.database.models.base import Base
from app.database.database import engine

setup_logging(logging.INFO)
app = FastAPI()
setup_cors(app, ALLOWED_HOSTS)
route.include_routers()

app.include_router(
    route.router,
    prefix='/api'
)

app.include_router(
    auth_controller.router,
    tags=['auth']
)


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logging.info("Application has started")
        


@app.on_event("shutdown")
async def shutdown():
    # Закрываем соединение с базой данных при завершении работы
    await engine.dispose()
    logging.info("The application is disabled")