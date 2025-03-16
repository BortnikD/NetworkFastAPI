import logging
from fastapi import FastAPI

from app.infrastructure.database.database import engine
from app.adapters.api.routes.route import setup_routers
from app.infrastructure.settings.logger import setup_logging
from app.infrastructure.middlewares.cors import setup_cors
from app.infrastructure.admin.admin import setup_admin

setup_logging(logging.INFO)
app = FastAPI()
setup_cors(app)
setup_admin(app)
setup_routers(app)


@app.on_event("startup")
async def startup():
    logging.info("Application has started")
        


@app.on_event("shutdown")
async def shutdown():
    await engine.dispose()
    logging.info("The application is disabled")
    


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)