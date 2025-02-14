from fastapi import FastAPI

from .api.v1.routes import user_controller, post_controller
from .models.base import Base
from app.database import engine

app = FastAPI()


@app.on_event("startup")
def startup():
    # Создание всех таблиц в базе данных (если они еще не созданы)
    Base.metadata.create_all(bind=engine)


app.include_router(
    user_controller.router,
    prefix='/api/v1',
    tags=['users']
)

app.include_router(
    post_controller.router,
    prefix='/api/v1',
    tags=['posts']
)