from fastapi import APIRouter, Depends, HTTPException

from app.domain.dto.profile import ProfilePublic
from app.domain.exceptions.user import UserDoesNotExist

from app.services.core_services.profile_service import ProfileService
from app.dependencies.services.profile import get_profile_service

router = APIRouter(prefix='/profiles')


@router.get('/{user_id}', response_model=ProfilePublic)
async def get_profile(
    user_id: int,
    profile_service: ProfileService = Depends(get_profile_service)
):
    """Получение профиля пользователя по ID."""
    try:
        return await profile_service.get_by_user_id(user_id)
    except UserDoesNotExist as e:
        raise HTTPException(status_code=404, detail=e.message)
