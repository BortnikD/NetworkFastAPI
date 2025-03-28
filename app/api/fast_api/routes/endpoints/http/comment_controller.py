from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    Path,
    Query,
    HTTPException
)

from app.domain.dto.pagination import CommentPagination, PaginatedResponse
from app.domain.dto.comment import (
    CommentCreate,
    CommentPublic,
    CommentUpdate
)
from app.domain.exceptions.base import AccessError
from app.domain.exceptions.comment import (
    CommentDoesNotExist,
    CommentUpdateError,
)

from app.infrastructure.database.models.user import User
from app.services.core_services.comment_service import CommentService
from app.dependencies.services.comment import get_comment_service
from app.dependencies.auth import get_current_active_user

router = APIRouter(prefix='/comments')


@router.post('/', response_model=CommentPublic)
async def create_comment(
    comment: CommentCreate,
    current_user: User = Depends(get_current_active_user),
    comment_service: CommentService = Depends(get_comment_service)
):
    """Создает новый комментарий от имени текущего пользователя."""
    return await comment_service.save(comment, current_user.id)


@router.get('/{post_id}', response_model=PaginatedResponse)
async def read_comments(
    pagination: Annotated[CommentPagination, Query()],
    post_id: int = Path(gt=0),
    comment_service: CommentService = Depends(get_comment_service)
):
    """Получает комментарии к посту с пагинацией."""
    return await comment_service.get_all_by_post_id(post_id, pagination.offset, pagination.limit)


@router.patch('/', response_model=CommentPublic)
async def update_comment(
    comment: CommentUpdate,
    current_user: User = Depends(get_current_active_user),
    comment_service: CommentService = Depends(get_comment_service)
):
    """Обновляет комментарий, если он принадлежит текущему пользователю."""
    try:
        return await comment_service.update(comment, current_user.id)
    except CommentDoesNotExist as e:
        raise HTTPException(status_code=404, detail=e.message)
    except AccessError as e:
        raise HTTPException(status_code=403, detail=e.message)
    except CommentUpdateError as e:
        raise HTTPException(status_code=400, detail=e.message)


@router.delete('/{comment_id}')
async def delete_comment(
    comment_id: int = Path(gt=0),
    current_user: User = Depends(get_current_active_user),
    comment_service: CommentService = Depends(get_comment_service)
):
    """Удаляет комментарий, если он принадлежит текущему пользователю."""
    try:
        await comment_service.delete(comment_id, current_user.id)
    except CommentDoesNotExist as e:
        raise HTTPException(status_code=404, detail=e.message)
    except AccessError as e:
        raise HTTPException(status_code=403, detail=e.message)
    except CommentUpdateError as e:
        raise HTTPException(status_code=400, detail=e.message)

