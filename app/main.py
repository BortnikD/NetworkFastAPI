from fastapi import FastAPI
import logging

from app.api.v1.routes import base_controller
from app.database.models.base import Base
from app.database.database import engine
from app.dependecies import auth

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s | %(asctime)s | %(name)s |  %(message)s",
        handlers=[
        logging.FileHandler("app/core/app.log"),  # Логи будут записываться в файл app.log
        logging.StreamHandler()  # Логи также будут выводиться в консоль
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
def startup():
    Base.metadata.create_all(bind=engine)


