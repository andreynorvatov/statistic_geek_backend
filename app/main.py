from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from app.api.main import api_router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    # docs_url=None,
    # redoc_url=None,
    # openapi_url=f"{settings.API_V1_STR}/openapi.json",
    # openapi_url=None if settings.srv.ENVIRONMENT not in settings.srv.SHOW_DOCS_ENVIRONMENT else settings.srv.OPENAPI_URL,
    default_response_class=ORJSONResponse,
)

app.include_router(api_router,
                   # prefix=settings.API_V1_STR
                   )
