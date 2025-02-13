from sqlalchemy.orm import Session
from fastapi import status

from app.schemas.user import UserCreate, UserPublic
from app.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, db: Session):
        self.user_repository = UserRepository(db)

    def create_user(self, user_create: UserCreate) -> UserPublic :
        existing_user = self.user_repository.get_user_by_email(user_create.email)
        if existing_user:
            raise ValueError("Пользователь с таким email уже существует.")
        
        user = self.user_repository.create_user(user_create)
        return user

    def get_users(self, offset: int, limit: int) -> list[UserPublic]:
        return self.user_repository.get_users(offset, limit)
    
    def get_user_by_id(self, id: int):
        user = self.user_repository.get_user_by_id(id)
        if user:
            return user
        else:
            raise status.HTTP_404_NOT_FOUND

