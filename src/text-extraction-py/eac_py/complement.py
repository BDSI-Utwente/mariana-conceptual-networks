from pathlib import Path
import difflib


def complement(a: str, b: str, debug: bool = False) -> str:
    source = a.split("\n")
    target = b.split("\n")

    diff = list(difflib.ndiff(source, target))
    new = ""

    for i, line in enumerate(diff):
        if debug:
            print(line)

        if line.startswith("+") and (
            (len(diff) > i and not diff[i].startswith("?")) or len(diff) <= i
        ):
            new = new + line[2:] + "\n"
    return new
