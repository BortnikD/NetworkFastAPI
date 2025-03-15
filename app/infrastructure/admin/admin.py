import logging
from fastapi import FastAPI
from sqladmin import Admin

from app.infrastructure.database.database import engine
from app.infrastructure.admin.views import setup_views


def setup_admin(app: FastAPI) -> None:
    admin = Admin(app=app, engine=engine)
    setup_views(admin)
    logging.info("Admin configured")