from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.api.dependencies.db import get_db
from app.core.dto.profile import ProfilePublic
from app.core.services.profile_service import ProfileService

router = APIRouter(
    prefix='/profiles'
)


@router.get('/{user_id}')
async def get_profile(user_id: int, db: AsyncSession = Depends(get_db)) -> ProfilePublic:
    service = ProfileService(db)
    return await service.get_profile_by_id(user_id)