from abc import ABC, abstractmethod

import cv2
import numpy as np


class ImageEnhancement(ABC):
    """Абстрактный базовый класс для улучшения изображения"""

    @abstractmethod
    def enhance(self, image: np.ndarray) -> np.ndarray:
        """Применяет улучшение к изображению"""
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Возвращает название улучшения"""
        pass


class UpscaleEnhancement(ImageEnhancement):
    """Увеличение размера изображения для улучшения читаемости"""

    def __init__(self, scale_factor: float = 2.0):
        self.scale_factor = scale_factor

    def enhance(self, image: np.ndarray) -> np.ndarray:
        new_width = int(image.shape[1] * self.scale_factor)
        new_height = int(image.shape[0] * self.scale_factor)
        return cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_CUBIC)

    @property
    def name(self) -> str:
        return f"Upscale (x{self.scale_factor})"


class ContrastEnhancement(ImageEnhancement):
    """Улучшение контрастности изображения"""

    def enhance(self, image: np.ndarray) -> np.ndarray:
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        lab_planes = list(cv2.split(lab))
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        lab_planes[0] = clahe.apply(lab_planes[0])
        lab = cv2.merge(lab_planes)
        return cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

    @property
    def name(self) -> str:
        return "Contrast Enhancement"


class SharpnessEnhancement(ImageEnhancement):
    """Повышение резкости изображения"""

    def enhance(self, image: np.ndarray) -> np.ndarray:
        kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
        return cv2.filter2D(image, -1, kernel)

    @property
    def name(self) -> str:
        return "Sharpness Enhancement"


class BinarizationEnhancement(ImageEnhancement):
    """Бинаризация для выделения контуров"""

    def enhance(self, image: np.ndarray) -> np.ndarray:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)

    @property
    def name(self) -> str:
        return "Binarization Enhancement"


class DenoisingEnhancement(ImageEnhancement):
    """Подавление шумов"""

    def enhance(self, image: np.ndarray) -> np.ndarray:
        return cv2.medianBlur(image, 3)

    @property
    def name(self) -> str:
        return "Denoising Enhancement"
