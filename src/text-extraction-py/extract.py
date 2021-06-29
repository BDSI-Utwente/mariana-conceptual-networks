import argparse
from tika import parser
from pathlib import Path
import fitz
from tempfile import mkstemp
from docx2pdf import convert
from os import remove


def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTIONS] FILE...",
        description="Extract text from documents.",
    )
    parser.add_argument(
        "files",
        nargs="+",
        metavar="FILE",
        help="one or more files to extract text from",
    )
    parser.add_argument(
        "-o",
        "--outdir",
        dest="outdir",
        help="path to output directory (default: current working directory)",
    )
    return parser


def main() -> None:
    args = init_argparse().parse_args()
    if args.outdir:
        out_dir = Path(args.outdir)
    else:
        out_dir = Path.cwd()

    for source in args.files:
        sourcePath = Path(source)
        targetPath = out_dir.joinpath(sourcePath.with_suffix(".txt").name)
        content = extract_text(sourcePath)

        print(f"{sourcePath.name} -> {targetPath.name}")

        with open(targetPath, "wb") as target:
            target.write(content.encode("utf8"))


def extract_text(path: Path, page: int = -1) -> str:
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


if __name__ == "__main__":
    main()
