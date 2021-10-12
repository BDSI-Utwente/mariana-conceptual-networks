import argparse
from typing import Union
from tika import parser
from pathlib import Path
import fitz
from docx2pdf import convert
from os import remove


def extract_text(path: Union[Path, str], page: int = -1) -> str:
    if isinstance(path, str):
        path = Path(path)
    if path.suffix == ".pdf":
        return extract_text_pdf(path, page)
    if path.suffix == ".docx":
        return extract_text_docx(path, page)
    else:
        # tika (docx) doesn't do pages
        return extract_text_tika(path)


def extract_text_pdf(path: Path, page: int = -1) -> str:
    with fitz.open(path) as pdf:
        if page >= 0:
            return pdf.get_page_text(0).strip()
        return str.join("", (page.get_text() for page in pdf)).strip()


def extract_text_docx(path: Path, page: int = -1) -> str:
    if page < 0:
        return extract_text_tika(path)

    temp_file = path.with_suffix(".tmp.pdf")

    print(f"{path} -> {temp_file}")
    convert(path, temp_file)
    content = extract_text_pdf(temp_file, page)
    remove(temp_file)
    return content


def extract_text_tika(path: Path) -> str:
    return parser.from_file(str(path))["content"].strip()
