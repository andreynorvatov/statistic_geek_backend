import cv2
from pyzbar.pyzbar import decode  # type: ignore

from app.api.qr_code_recognize.qr_code_enhancer import qr_code_enhancement_pipeline
from app.logger import logger


def is_double_encoded_cp1251(text: str) -> bool:
    """
    Проверяет, является ли текст результатом двойного кодирования (CP1251 → UTF-8)
    """
    try:
        # Пробуем преобразовать как двойную закодированную строку
        latin1_bytes = text.encode("latin-1")
        cp1251_text = latin1_bytes.decode("cp1251")

        # Если после преобразования получилась читаемая строка - это двойное кодирование
        # Проверяем, что в результате есть кириллические символы
        cyrillic_chars = any("А" <= char <= "я" for char in cp1251_text if char.isalpha())

        return cyrillic_chars
    except (UnicodeEncodeError, UnicodeDecodeError):
        return False


def decode_double_encoded(data_bytes: bytes) -> str | None:
    """Декодирует данные с двойным кодированием"""
    try:
        corrupted_text = data_bytes.decode("utf-8")
        latin1_bytes = corrupted_text.encode("latin-1")
        correct_text = latin1_bytes.decode("cp1251")
        return correct_text
    except (UnicodeDecodeError, UnicodeEncodeError):
        return None


def decode_qr_data(data_bytes: bytes) -> dict[str, str | None | bool]:
    """
    Корректно декодирует данные QR-кода с двойным кодированием
    """
    try:
        corrupted_text = data_bytes.decode("utf-8")
        is_double = is_double_encoded_cp1251(corrupted_text)

        if is_double:
            data = decode_double_encoded(data_bytes)
            success = data is not None
        else:
            data = corrupted_text
            success = True

        return {"data": data, "double_encoded": is_double, "success": success}

    except UnicodeDecodeError:
        return {"data": None, "double_encoded": False, "success": False}


def handle_decoded_objects(decoded_objects, enhancement_name: str, img_path: str) -> dict[str, str] | None:
    """Обрабатывает результат распознавания QR-кода и возвращает декодированные данные"""
    if not decoded_objects:
        logger.warning(f"[{enhancement_name}] QR-код не найден на {img_path}")
        return None

    logger.info(f"[{enhancement_name}] QR-код распознан на {img_path}")

    for obj in decoded_objects:
        decoded_qr_data = decode_qr_data(obj.data)

        if decoded_qr_data.get("success"):
            return {
                "data": decoded_qr_data.get("data"),
                "type": obj.type,
                "rect": obj.rect,
                "polygon": obj.polygon,
                "quality": obj.quality,
                "orientation": obj.orientation,
                "double_encoded": decoded_qr_data.get("double_encoded"),
                "file_name": img_path,
            }
        else:
            return {
                "data": decoded_qr_data.get("data"),
                "double_encoded": decoded_qr_data.get("double_encoded"),
                "file_name": img_path,
            }


def enhance_and_recognize_qr_code(
    img_path: str, enhancement_pipeline: list = qr_code_enhancement_pipeline
) -> dict[str, str] | None:
    original_image = cv2.imread(img_path)

    if original_image is None:
        logger.warning(f"Ошибка: не удалось загрузить изображение {img_path}")
        return None

    # Пробуем распознать без улучшений
    decoded_objects = decode(original_image)
    result = handle_decoded_objects(decoded_objects, "Без улучшения", img_path)
    if result:
        return result

    # Пробуем с улучшениями (каждое применяется к оригинальному изображению)
    for enhancement in enhancement_pipeline:
        enhanced_image = enhancement.enhance(original_image)
        decoded_objects = decode(enhanced_image)

        result = handle_decoded_objects(decoded_objects, enhancement.name, img_path)
        if result:
            return result

    logger.warning(f"Не удалось распознать QR-код после всех улучшений: {img_path}")
    return None


def parse_qr_data(data: str) -> dict[str, str]:
    """Парсинг данных QR-кода оплаты"""

    fields = data.split("|")
    result = {}

    for field in fields:
        if "=" in field:
            key, value = field.split("=", 1)
            if key == "Sum":
                value = ",".join([value[:-2], value[-2:]])

            result[key] = value

    return result


def get_qr_code_data(file_path: str) -> dict[str, str] | None:
    qr_content = enhance_and_recognize_qr_code(file_path)

    if not qr_content:
        logger.warning(f"QR-код не найден в файле: {file_path}")
        return

    else:
        if qr_content.get("data").startswith("ST"):
            return parse_qr_data(qr_content.get("data"))
        else:
            # TODO возврат текста "QR код не для оплаты квитаници
            return qr_content.get("data")


# BASE_DIR = r"C:\GIT_PROJECTS\utility_bills_archive\photo_saver_tg_bot\saved_photos\pnv\photo_600.jpg"
# r = enhance_and_recognize_qr_code(BASE_DIR)
# print(r)
# print("---")
#
# for k, v in r.items():
#     print(f"{k}: {v}")
#


# BASE_DIR = r"C:\GIT_PROJECTS\utility_bills_archive\photo_saver_tg_bot\saved_photos"
# qr_files = [f for f in os.listdir(BASE_DIR)
#             if os.path.isfile(os.path.join(BASE_DIR, f)) and
#             f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp', '.tiff'))]
# # print(qr_files)
# qr_files_cnt = len(qr_files)
# for cnt, filename in enumerate(qr_files, 1):
#     print(f" {cnt}/{qr_files_cnt} Обработка {filename}")
#
#     file_path = os.path.join(BASE_DIR, filename)
#     # r = enhance_and_recognize_qr_code(file_path)
#     r = get_qr_code_data(file_path)
#     print(r)
#
# print("Fine))")
