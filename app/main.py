import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.infrastructure.database.database import engine
from app.api.fast_api.routes.route import setup_routers
from app.infrastructure.settings.logger import setup_logging
from app.infrastructure.middlewares.cors import setup_cors
from app.services.admin.admin import setup_admin

setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("lifespan started")
    yield
    await engine.dispose()
    logging.info("The database connection is disabled")


app = FastAPI(lifespan=lifespan)
setup_cors(app)
setup_admin(app)
setup_routers(app)
