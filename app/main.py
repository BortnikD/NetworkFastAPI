from fastapi import FastAPI

from .api.v1.routes import base_controller
from .models.base import Base
from app.database import engine

app = FastAPI()

app.include_router(
    base_controller.router,
    prefix='/api/v1'
)


@app.on_event("startup")
def startup():
    # Создание всех таблиц в базе данных (если они еще не созданы)
    Base.metadata.create_all(bind=engine)


