import argparse

from scanner import DocumentScanner
from scanner.ocr_engine import OcrEngine


def parse_args():
    p = argparse.ArgumentParser(description='Сканер документов: PDF -> TXT/DOCX')
    p.add_argument('input', help='Путь к PDF')
    p.add_argument('output', help='Результат: file.txt или file.docx')
    p.add_argument('--lang', default='rus+eng', help='Языки Tesseract')
    p.add_argument('--dpi', type=int, default=300)
    p.add_argument('--force-ocr', action='store_true',
                   help='Игнорировать текстовый слой PDF')
    p.add_argument('--debug-dir', help='Сохранять обработанные страницы')
    p.add_argument('--tesseract', help='Путь к tesseract')
    return p.parse_args()


def main():
    args = parse_args()
    scanner = DocumentScanner(
        ocr=OcrEngine(lang=args.lang, tesseract_cmd=args.tesseract),
        dpi=args.dpi,
        force_ocr=args.force_ocr,
        debug_dir=args.debug_dir,
    )
    scanner.scan(args.input, args.output)


if __name__ == '__main__':
    main()