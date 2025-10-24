from pathlib import Path
from typing import Any

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from app.api.file_storage.utils import get_file_path_by_uuid, save_file
from app.api.qr_code_recognize.enhance_and_recognize_qr_code import get_qr_code_data

file_storage_router = APIRouter()

_ROOT_DIRECTORY: Path = Path(__file__).resolve().parent.parent.parent.parent
BASE_STORAGE_PATH = Path.joinpath(_ROOT_DIRECTORY, "file_storage")


def validate_image_content_type(
    file: UploadFile = File(..., description="Изображение для загрузки"),
) -> UploadFile:
    """
    Dependency для проверки типа контента изображения
    """
    allowed_content_types = ["image/jpeg", "image/png", "image/gif", "image/webp"]

    if file.content_type not in allowed_content_types:
        raise HTTPException(
            status_code=400,
            detail="Недопустимый тип файла. Разрешены только изображения (JPEG, PNG, GIF, WebP)",
        )

    return file


@file_storage_router.post("/upload-image/")
async def upload_image(file: UploadFile = Depends(validate_image_content_type)) -> dict[str, Any]:
    """
    Эндпоинт для загрузки изображения (jpeg, png, gif, webp)
    """
    try:
        # Загрузка файла
        uploaded_file_data = await save_file(file, BASE_STORAGE_PATH)

        return {
            **uploaded_file_data,
            "file_name": file.filename,
            "content_type": file.content_type,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при сохранении файла {file.filename}: {str(e)}")
    finally:
        await file.close()


@file_storage_router.post("/get-qr-code-data/")
async def qr_code_data(file: UploadFile = Depends(validate_image_content_type)) -> dict[str, Any]:
    """
    Эндпоинт для получения данных QR-code
    """
    try:
        # Загрузка файла
        uploaded_file_data = await save_file(file, BASE_STORAGE_PATH)

        file_path = get_file_path_by_uuid(uploaded_file_data.get("file_id"), BASE_STORAGE_PATH)
        qr_code_data_result = get_qr_code_data(file_path)

        return {
            "qr_code_data_result": qr_code_data_result,
            **uploaded_file_data,
            "file_name": file.filename,
            "content_type": file.content_type,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при сохранении файла {file.filename}: {str(e)}")
    finally:
        await file.close()
