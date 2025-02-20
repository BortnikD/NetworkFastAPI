import logging
import os
import shutil
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Path
from starlette.responses import FileResponse

from app.database.models.user import User
from app.dependecies.db import get_db
from app.dependecies.auth import get_current_user
from app.services.image_service import ImageService
from app.core.config import POSTS_IMAGES_DIR, BASE_URL

router = APIRouter(
    prefix='/images'
)


@router.post('/upload/')
async def upload_image(post_id: int,
                       file: UploadFile = File(...),
                       db: AsyncSession = Depends(get_db),
                       current_user: User = Depends(get_current_user)):
    image_service = ImageService(db)
    user_folder = os.path.join(POSTS_IMAGES_DIR, current_user.username)
    os.makedirs(user_folder, exist_ok=True)

    file_path = os.path.abspath(os.path.join(user_folder, file.filename))

    with open(file_path, 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)


    # Генерируем URL для скачивания
    relative_path = os.path.join(current_user.username, file.filename)
    relative_path = relative_path.replace("\\", "/")  # Приведение пути к единому виду
    download_url = f"{BASE_URL}/api/v1/images/download/{relative_path}"

    # Сохраняем в БД ссылку вместо абсолютного пути
    await image_service.upload_image(download_url, current_user.id, post_id)

    return {
        'filename': file.filename,
        'download_url': download_url
    }


@router.get("/download/{file_path:path}")
async def download_file(file_path: str):
    """
    Возвращает файл, расположенный по указанному пути относительно базовой директории POSTS_IMAGES_DIR.
    Параметр file_path защищён от попыток обхода (directory traversal).
    """
    base_path = os.path.abspath(POSTS_IMAGES_DIR)
    # Собираем полный путь к запрашиваемому файлу внутри базовой директории
    requested_path = os.path.abspath(os.path.join(base_path, file_path))

    # Проверяем, что запрашиваемый путь находится внутри base_path
    if not requested_path.startswith(base_path):
        raise HTTPException(status_code=400, detail="Некорректный путь к файлу")

    if not os.path.exists(requested_path):
        raise HTTPException(status_code=404, detail="Файл не найден")

    return FileResponse(requested_path)

