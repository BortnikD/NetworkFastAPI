from typing import Generator
from sqlalchemy.orm import Session

from app.database.database import SessionLocal


def get_db() -> Generator[Session]:
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()