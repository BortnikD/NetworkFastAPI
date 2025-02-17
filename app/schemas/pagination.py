from pydantic import BaseModel, Field, HttpUrl
from typing import Optional


class UsersPagination(BaseModel):
    offset: int = Field(default=0, ge=0, description="Смещение от начала списка")
    limit: int = Field(default=10, gt=0, le=100, description="Количество элементов на странице")


class PostPagination(BaseModel):
    offset: int = Field(default=0, ge=0, description="Смещение от начала списка")
    limit: int = Field(default=5, gt=0, le=100, description="Количество элементов на странице")


class CommentPagination(BaseModel):
    offset: int = Field(default=0, ge=0, description="Смещение от начала списка")
    limit: int = Field(default=5, gt=0, le=100, description="Количество элементов на странице")
    

class PaginatedResponse(BaseModel):
    count: int = Field(description="Количество записей", examples=[30])
    prev: Optional[HttpUrl] = Field(default=None, description="url предыдущей страницы", examples=['https://interesly.com/api/v1/users?offset=<page-1>&limit=<limit>'])
    next: Optional[HttpUrl] = Field(default=None, description="url следующей страницы",  examples=['https://interesly.com/api/v1/users?offset=<page+1>&limit=<limit>'])
    results: Optional[list] = Field(default=[], description='Записи',  examples=[['some_objects']]) 