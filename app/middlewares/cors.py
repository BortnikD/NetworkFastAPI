import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def setup_cors(app: FastAPI, allowed_hosts: list[str]) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_hosts,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    logging.info(f"CORS configured with: {allowed_hosts}")