from abc import ABC, abstractmethod
from pathlib import Path

from docx import Document


class BaseExporter(ABC):
    @abstractmethod
    def save(self, pages: list[str], path: str) -> None:
        ...


class TxtExporter(BaseExporter):
    def save(self, pages: list[str], path: str) -> None:
        body = "\n\n".join(pages)
        Path(path).write_text(body, encoding='utf-8')


class DocxExporter(BaseExporter):
    def save(self, pages: list[str], path: str) -> None:
        doc = Document()
        for i, text in enumerate(pages, start=1):
            doc.add_heading(f'Страница {i}', level=2)
            for paragraph in text.split("\n\n"):
                if paragraph.strip():
                    doc.add_paragraph(paragraph.strip())
            if i < len(pages):
                doc.add_page_break()
        doc.save()


def get_exporter(path: str) -> BaseExporter:
    """Фабрика: выбирает экспортер по расширению файла"""
    ext = Path(path).suffix.lower()
    exporters = {'.txt': TxtExporter, '.docx': DocxExporter}
    if ext not in exporters:
        raise ValueError(f'Неподдерживаемый формат: {ext}. Используйте .txt или .docx')
    return exporters[ext]()