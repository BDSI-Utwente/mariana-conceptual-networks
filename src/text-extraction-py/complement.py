from pathlib import Path
from extract import extract_text
import argparse
import difflib


def __init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTIONS] FILE_A FILE_B",
        description="Extracts text from two files, and returns content in file B that is not present in file A.",
    )
    parser.add_argument(
        "fileA",
        metavar="FILE_A",
        help="Source file, usually a previous version of a document",
    )
    parser.add_argument(
        "fileB",
        metavar="FILE_B",
        help="Target file, usually a newer version of a document",
    )
    return parser


def complement(a: str, b: str) -> str:
    source = a.split("\n")
    target = b.split("\n")

    diff = list(difflib.ndiff(source, target))
    new = ""

    for i, line in enumerate(diff):
        if line.startswith("+") and len(diff) > i + 1 and not diff[i].startswith("?"):
            new = new + line[2:] + "\n"
    return new


def __main():
    args = __init_argparse().parse_args()
    new = complement(extract_text(Path(args.fileA)), extract_text(Path(args.fileB)))
    print(new)


if __name__ == "__main__":
    __main()
