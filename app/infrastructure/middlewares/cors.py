import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.infrastructure.settings.config import ALLOWED_HOSTS


def setup_cors(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_HOSTS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    logging.info(f"CORS configured with: {ALLOWED_HOSTS}")