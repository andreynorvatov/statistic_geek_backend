from datetime import datetime

from fastapi import APIRouter, status

from app.api.system_api.health_check.models import HealthCheck
from app.core.config import settings
from app.logger import logger

health_check_router = APIRouter()

@health_check_router.get(
    "/health/detailed",
    response_model=HealthCheck,
    status_code=status.HTTP_200_OK,
    summary="Проверка состояния приложения",
    description="Дополнительная информация: Полные данные о приложении",
)
async def health_check_detailed() -> HealthCheck:
    health_data = {
        "status": "OK",
        "environment": settings.ENVIRONMENT,
        "version": settings.VERSION,
        "timestamp": datetime.now(),
    }
    logger.info(f"{health_data}")
    return HealthCheck(**health_data)
