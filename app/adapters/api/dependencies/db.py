from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import AsyncSessionLocal


# Функция зависимости для получения сессии в эндпоинтах FastAPI
async def get_db() -> AsyncGenerator[AsyncSession]:
    async with AsyncSessionLocal() as session:
        yield session