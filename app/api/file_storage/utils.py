import os
from pathlib import Path
from typing import Any
from uuid import uuid4

import aiofiles  # type: ignore
from fastapi import UploadFile

from app.logger import logger


def get_img_name_uuid4() -> str:
    # Генерируем UUID и возвращаем как строку
    return str(uuid4())


async def save_file(
        uploaded_file: UploadFile,
        base_storage_path: Path,
        chunk_size: int = 500 * 1024
) -> dict[str, Any]:
    """
    Сохранение файла на диск с созданием структуры по uuid
    :param uploaded_file: Файл
    :param base_storage_path: Путь файлового хранилища
    :param chunk_size: Конфигурируемый размер чанка для сохранения фала)
    :return:
    {
        "file_id": uuid_str,
        "file_size_byte": len(content)
    }
    """
    # Генерируем UUID
    uuid_str = get_img_name_uuid4()

    # Извлекаем части для пути (первые 2 символа, следующие 2)
    first_part, second_part = uuid_str[:2], uuid_str[2:4]

    # Формируем полный путь для сохранения
    target_dir = base_storage_path / first_part / second_part

    # Создаем директории, если их нет
    target_dir.mkdir(parents=True, exist_ok=True)

    # Формируем полное имя файла с исходным расширением
    file_extension = Path(uploaded_file.filename).suffix if uploaded_file.filename is not None else ""
    target_filename = f"{uuid_str}{file_extension}"
    full_file_path = target_dir / target_filename

    # Если нужно проверить размер до сохранения
    content = await uploaded_file.read()
    file_size = len(content)

    # Сохраняем файл частями:
    await uploaded_file.seek(0)
    async with aiofiles.open(full_file_path, 'wb') as f:
        c = 0
        while chunk := await uploaded_file.read(chunk_size):
            c += 1
            logger.debug(f"chunk: {c}")
            await f.write(chunk)

    logger.info(f"Фото сохранено: {uuid_str} ({file_size} байт)")

    return {
        "file_id": uuid_str,
        "file_size_byte": file_size
    }


def get_file_path_by_uuid(file_uuid: str, base_storage_path: Path) -> str:
    """Функция для получения пути к файлу по его UUID"""
    uuid_str = file_uuid
    first_part = uuid_str[0:2]
    second_part = uuid_str[2:4]
    file_extension = ".jpg"  # Это нужно знать или хранить в БД
    return os.path.join(base_storage_path, first_part, second_part, f"{uuid_str}{file_extension}")
