import logging

from fastapi import FastAPI
from sqladmin import Admin

from app.infrastructure.database.database import engine
from app.adapters.admin.views import setup_views
from app.adapters.admin.security import AdminAuthenticationBackend
from app.infrastructure.settings.config import AUTH_KEY, BASE_URL


def setup_admin(app: FastAPI) -> None:
    authentication_backend = AdminAuthenticationBackend(AUTH_KEY)
    admin = Admin(app=app, engine=engine, authentication_backend=authentication_backend)
    setup_views(admin)
    logging.info(f"Admin configured on {BASE_URL}/admin")