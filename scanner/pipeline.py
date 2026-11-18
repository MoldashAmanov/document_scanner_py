from pathlib import Path
import cv2

from .exporters import get_exporter
from .ocr_engine import OcrEngine
from .pdf_loader import PdfLoader
from .preprocessor import ImagePreprocessor


class DocumentScanner:
    """Полный цикл: PDF -> обработка -> OCR -> файл"""

    MIN_TEXT_LAYER = 20 # меньше символов - считаем, что это скан

    def __init__(self, preproccesor: ImagePreprocessor | None = None,
                 ocr: OcrEngine | None = None, dpi: int = 300,
                 force_ocr: bool = False, debug_dir: str | None = None):
        self.preproccesor = preproccesor or ImagePreprocessor()
        self.ocr = ocr or OcrEngine()
        self.dpi = dpi
        self.force_ocr = force_ocr
        self.debug_dir = Path(debug_dir) if debug_dir else None
        if self.debug_dir:
            self.debug_dir.mkdir(parents=True, exist_ok=True)

    def scan(self, pdf_path: str, output_path: str) -> list[str]:
        pages: list[str] = []
        with PdfLoader(pdf_path) as loader:
            total = len(loader)
            for i in range(total):
                print(f'Страница {i + 1} / {total}...')
                pages.append(self._process_pages(loader, i))
        get_exporter(output_path).save(pages, output_path)
        print(f'Готово: {output_path}')
        return pages

    def _process_pages(self, loader: PdfLoader, index: int) -> str:
        if not self.force_ocr:
            text = loader.extract_text_layer(index)
            if len(text) > self.MIN_TEXT_LAYER:
                return text

        image = loader.render_page(index, self.dpi)
        processed = self.preproccesor.process(image)
        if self.debug_dir:
            cv2.imwrite(str(self.debug_dir / f'page_{index + 1}.png'), processed)
        return self.ocr.recognize(processed)