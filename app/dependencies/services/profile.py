from fastapi import Depends

from app.services.use_cases.profile_service import ProfileService
from app.infrastructure.database.repositories.profile_repository import ProfileRepository
from app.dependencies.db import get_db


def get_profile_service(db=Depends(get_db)) -> ProfileService:
    profile_repo = ProfileRepository(db)
    return ProfileService(profile_repo)