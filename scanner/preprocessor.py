import cv2
import numpy as np


class ImagePreprocessor:
    """Подготавливает изображение страницы в OCR"""

    def __init__(self, denoise: bool = True, deskew: bool = True,
                 binarize: bool = True):
        self.denoise = denoise
        self.deskew = deskew
        self.binarize = binarize

    def process(self, image: np.ndarray) -> np.ndarray:
        gray = self._to_gray(image)
        if self.denoise:
            gray = cv2.fastNlMeansDenoising(gray, None, h=10)
        if self.deskew:
            gray = self._deskew(gray)
        if self.binarize:
            gray = self._binarize(gray)
        return gray

    @staticmethod
    def _to_gray(image: np.ndarray) -> np.ndarray:
        if image.ndim == 3:
            return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return image

    @staticmethod
    def _binarize(gray: np.ndarray) -> np.ndarray:
        """Адаптивный порог хорошо работает при неровном освещениее"""
        return cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, blockSize=31, C=15)

    @staticmethod
    def _rotate(image: np.ndarray, angle: float) -> np.ndarray:
        h, w = image.shape[:2]
        matrix = cv2.getRotationMatrix2D((w / 2, h / 2), angle, 1.0)
        return cv2.warpAffine(image, matrix, (w, h),
                              flags=cv2.INTER_CUBIC,
                              borderMode=cv2.BORDER_CONSTANT,
                              borderValue=255)

    def _estimate_skew(self, gray: np.ndarray) -> float:
        """Ищет угол, при котором строки текста максимально 'горизонтальны'
        Метод проекционного профиля: у ровного текста сумма пикселей по
        строкам сильно колеблется (строки и пробелы между ними), поэтому
        дисперсия профиля максимальна
        """
        scale = 600 / gray.shape[1]
        small = cv2.resize(gray, None, fx=scale, fy=scale)
        _, inv = cv2.threshold(small, 0, 255,
                               cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        best_angle, best_score = 0.0, -1.0
        for angle in np.arange(-10, 10.5, 0.5):
            rotated = self._rotate(inv, float(angle))
            score = np.var(rotated.sum(axis=1))
            if score > best_score:
                best_angle, best_score = float(angle), score
        return best_angle

    def _deskew(self, gray: np.ndarray) -> np.ndarray:
        angle = self._estimate_skew(gray)
        if abs(angle) < 0.2:
            return gray
        return self._rotate(gray, angle)
    
