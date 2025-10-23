from pathlib import Path
from typing import Any

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.api.file_storage.utils import save_file

file_storage_router = APIRouter()

_ROOT_DIRECTORY: Path = Path(__file__).resolve().parent.parent.parent.parent
BASE_STORAGE_PATH = Path.joinpath(_ROOT_DIRECTORY, "file_storage")

@file_storage_router.post("/upload-image/")
async def upload_image(
        file: UploadFile = File(..., description="Изображение для загрузки")
) -> dict[str, Any]:
    """
    Эндпоинт для загрузки изображения (jpeg, png, gif, webp)
    """
    # Проверяем, что файл является изображением
    allowed_content_types = ["image/jpeg", "image/png", "image/gif", "image/webp"]

    if file.content_type not in allowed_content_types:
        raise HTTPException(
            status_code=400,
            detail="Недопустимый тип файла. Разрешены только изображения (JPEG, PNG, GIF, WebP)"
        )

    try:
        # Загрузка файла
        uploaded_file_data = await save_file(file, BASE_STORAGE_PATH)

        return {
            **uploaded_file_data,
            "file_name": file.filename,
            "content_type": file.content_type,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при сохранении файла {file.filename}: {str(e)}"
        )
    finally:
        await file.close()
