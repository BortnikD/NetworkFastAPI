from fastapi import APIRouter, Depends
from app.core.dto.profile import ProfilePublic
from app.core.services.profile_service import ProfileService
from app.adapters.api.dependencies.services.profile import get_profile_service

router = APIRouter(prefix='/profiles')


@router.get('/{user_id}', response_model=ProfilePublic)
async def get_profile(
    user_id: int,
    profile_service: ProfileService = Depends(get_profile_service)
):
    """Получение профиля пользователя по ID."""
    return await profile_service.get_profile_by_id(user_id)
