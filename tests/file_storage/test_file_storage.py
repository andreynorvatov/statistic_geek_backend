from fastapi.testclient import TestClient

from app.main import app


def test_upload_image_success() -> None:
    """Тест успешной загрузки изображения"""
    client = TestClient(app)

    # Создаем тестовое изображение в памяти
    image_data = b"fake_image_data"
    files = {"file": ("test_image.jpg", image_data, "image/jpeg")}

    response = client.post("/file-storage/upload-image/", files=files)

    # Основные проверки
    assert response.status_code == 200

    response_data = response.json()
    assert "file_name" in response_data
    assert "content_type" in response_data
    assert response_data["file_name"] == "test_image.jpg"
    assert response_data["content_type"] == "image/jpeg"


def test_upload_image_invalid_file_type() -> None:
    """Тест загрузки файла неподдерживаемого типа"""
    client = TestClient(app)

    # Создаем файл с неподдерживаемым типом
    file_data = b"fake_text_data"
    files = {"file": ("test_file.txt", file_data, "text/plain")}

    response = client.post("/file-storage/upload-image/", files=files)

    # Проверяем ошибку
    assert response.status_code == 400
    response_data = response.json()
    assert "detail" in response_data
    assert "Недопустимый тип файла" in response_data["detail"]


def test_upload_image_no_file() -> None:
    """Тест запроса без файла"""
    client = TestClient(app)

    response = client.post("/file-storage/upload-image/")

    assert response.status_code == 422  # Validation error


def test_upload_image_different_image_types() -> None:
    """Тест загрузки различных поддерживаемых типов изображений"""
    client = TestClient(app)

    supported_types = [
        ("test_image.jpeg", "image/jpeg"),
        ("test_image.png", "image/png"),
        ("test_image.gif", "image/gif"),
        ("test_image.webp", "image/webp")
    ]

    for filename, content_type in supported_types:
        image_data = b"fake_image_data"
        files = {"file": (filename, image_data, content_type)}

        response = client.post("/file-storage/upload-image/", files=files)

        assert response.status_code == 200

        response_data = response.json()
        assert response_data["file_name"] == filename
        assert response_data["content_type"] == content_type


def test_upload_image_large_filename() -> None:
    """Тест загрузки изображения с длинным именем файла"""
    client = TestClient(app)

    long_filename = "a" * 100 + ".jpg"
    image_data = b"fake_image_data"
    files = {"file": (long_filename, image_data, "image/jpeg")}

    response = client.post("/file-storage/upload-image/", files=files)

    assert response.status_code == 200

    response_data = response.json()
    assert response_data["file_name"] == long_filename

