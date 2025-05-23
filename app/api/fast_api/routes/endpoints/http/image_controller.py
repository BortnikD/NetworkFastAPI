import os
import shutil

from fastapi import (
    APIRouter,
    Depends,
    UploadFile,
    File,
    HTTPException
)
from starlette.responses import FileResponse

from app.domain.entities.image import Image
from app.domain.dto.image import CreateImage
from app.domain.exceptions.image import (
    ImageIsEmptyError,
    ImageUploadError,
    ImageNotFoundError
)

from app.infrastructure.settings.config import POSTS_IMAGES_DIR, BASE_URL
from app.infrastructure.database.models.user import User
from app.services.core_services.image_service import ImageService
from app.dependencies.services.image import get_image_service
from app.dependencies.auth import get_current_user

router = APIRouter(prefix='/images')


@router.post('/upload/')
async def upload_image(
        post_id: int,
        file: UploadFile = File(...),
        current_user: User = Depends(get_current_user),
        image_service: ImageService = Depends(get_image_service)
        ):
    """Загрузка изображения и сохранение ссылки в БД."""

    user_folder = os.path.join(POSTS_IMAGES_DIR, current_user.username)
    os.makedirs(user_folder, exist_ok=True)

    file_path = os.path.abspath(os.path.join(user_folder, file.filename))

    with open(file_path, 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Генерируем URL для скачивания
    relative_path = os.path.join(current_user.username, file.filename).replace("\\", "/")
    download_url = f"{BASE_URL}/api/v1/images/download/{relative_path}"

    # Сохраняем ссылку в БД
    try:
        image = CreateImage(src=download_url, user_id=current_user.id, post_id=post_id)
        await image_service.upload(image)
    except ImageIsEmptyError as e:
        raise HTTPException(status_code=400, detail=e.message)
    except ImageUploadError as e:
        raise HTTPException(status_code=400, detail=e.message)
    except ImageNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)

    return {
        'filename': file.filename,
        'download_url': download_url
    }


@router.get("/download/{file_path:path}")
async def download_file(file_path: str):
    """
    Возвращает файл по пути, защищённому от directory traversal атак.
    """
    base_path = os.path.abspath(POSTS_IMAGES_DIR)
    requested_path = os.path.abspath(os.path.join(base_path, file_path))

    if not requested_path.startswith(base_path):
        raise HTTPException(status_code=400, detail="Некорректный путь к файлу")

    if not os.path.exists(requested_path):
        raise HTTPException(status_code=404, detail="Файл не найден")

    return FileResponse(requested_path)


@router.get('/get_sources/{post_id}')
async def get_sources_by_post_id(
        post_id: int,
        image_service: ImageService = Depends(get_image_service)
        ) -> list[Image]:
    """Получение списка изображений по ID поста."""
    try:
        return await image_service.get_sources_by_post_id(post_id)
    except ImageNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)
