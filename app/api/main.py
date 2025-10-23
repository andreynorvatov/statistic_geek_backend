from fastapi import APIRouter

from app.api.file_storage.api import file_storage_router
from app.api.system_api.health_check.api import health_check_router

api_router = APIRouter()


api_router.include_router(health_check_router, prefix="/system", tags=["Системные API"])
api_router.include_router(file_storage_router, prefix="/file-storage", tags=["API для работы с файлам"])
