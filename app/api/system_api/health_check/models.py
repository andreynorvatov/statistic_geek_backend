from datetime import datetime

from sqlmodel import SQLModel


# Модель только для Pydantic (без таблицы в БД)
class HealthCheck(SQLModel):
    status: str
    environment: str
    version: str
    timestamp: datetime
    # database_status: Optional[str] = None
