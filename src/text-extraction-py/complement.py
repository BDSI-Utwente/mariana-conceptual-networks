from pathlib import Path
import difflib


def complement(a: str, b: str) -> str:
    source = a.split("\n")
    target = b.split("\n")

    diff = list(difflib.ndiff(source, target))
    new = ""

    for i, line in enumerate(diff):
        if line.startswith("+") and len(diff) > i + 1 and not diff[i].startswith("?"):
            new = new + line[2:] + "\n"
    return new
