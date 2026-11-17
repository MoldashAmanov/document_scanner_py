import cv2
import fitz
import numpy as np


class PdfLoader:
    """Загружает PDF и отдает страницы как изображения или текст"""

    def __init__(self, path: str):
        self.path = path
        self._doc = fitz.open(path)

    def __len__(self) -> int:
        return self._doc.page_count

    def render_page(self, index: int, dpi: int = 300) -> np.ndarray:
        """Рендерит страницу в BGR-изображение"""
        page = self._doc[index]
        zoom = dpi / 72 # в PDF базовое разрешение 72 dpi
        pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom),
                              colorspace=fitz.csRGB, alpha=False)
        img = np.frombuffer(pix.samples, dtype=np.uint8)
        img = img.reshape(pix.height, pix.width, 3)
        return cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    def extract_text_layer(self, index: int) -> str:
        """Возвращает встроенный текст (пусто, если PDF - это скан)"""
        return self._doc[index].get_text().strip()

    def close(self) -> None:
        self._doc.close()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()