import numpy as np
import pytesseract


class OcrEngine:
    """Обертка над Tesseract"""

    def __init__(self, lang: str = 'rus+eng', psm: int = 3,
                 tesseract_cmd: str | None = None):
        self.lang = lang
        self.config = f'--oem 3 --psm {psm}'
        if tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

    def recognize(self, image: np.ndarray) -> str:
        text = pytesseract.image_to_string(image, lang=self.lang,
                                           config=self.config)
        return text.strip()
