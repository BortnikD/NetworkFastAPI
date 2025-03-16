from fastapi import Depends

from app.core.services.profile_service import ProfileService
from app.adapters.repositories.profile_repository import ProfileRepository
from app.adapters.dependencies.db import get_db


def get_profile_service(db=Depends(get_db)) -> ProfileService:
    profile_repo = ProfileRepository(db)
    return ProfileService(profile_repo)