from fastapi import APIRouter

from app.api.system_api.health_check.api import health_check_router

api_router = APIRouter()


api_router.include_router(health_check_router, prefix="/system", tags=["Системные API"])
