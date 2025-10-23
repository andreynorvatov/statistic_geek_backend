from datetime import datetime

from fastapi.testclient import TestClient

from app.main import app


def test_system_health() -> None:
    client = TestClient(app)
    response = client.get("/system/health/detailed")

    # Основные проверки статуса
    assert response.status_code == 200

    # Проверка структуры ответа
    json_data = response.json()

    # Проверка обязательных полей
    assert "status" in json_data
    assert "environment" in json_data
    assert "version" in json_data
    assert "timestamp" in json_data

    # Проверка значений полей
    assert json_data["status"] == "OK"
    assert json_data["environment"] in ["local", "production"]
    assert json_data["version"] is not None
    assert len(json_data["version"]) > 0

    # Проверка формата timestamp (должен быть строкой в ISO формате)
    try:
        datetime.fromisoformat(json_data["timestamp"].replace('Z', '+00:00'))
        timestamp_valid = True
    except (ValueError, TypeError):
        timestamp_valid = False
    assert timestamp_valid, "Timestamp должен быть в правильном формате"

    # Проверка типа данных
    assert isinstance(json_data["status"], str)
    assert isinstance(json_data["environment"], str)
    assert isinstance(json_data["version"], str)
    assert isinstance(json_data["timestamp"], str)
