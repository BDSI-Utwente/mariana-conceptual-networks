from pathlib import Path
import en_core_web_sm
import argparse
from fuzzywuzzy import process
from fuzzysearch import find_near_matches
from extract import extract_text
from re import compile

nlp = en_core_web_sm.load()


def __init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTIONS] FILE [ACTOR ...]",
        description="Anonymize file, removing provided actors and optionally extracting actors from the cover page.",
    )
    parser.add_argument(
        "file",
        metavar="FILE",
        help="file to anonymize",
    )
    parser.add_argument(
        "actors",
        nargs="*",
        metavar="ACTOR",
        help="named actors to remove",
    )
    parser.add_argument(
        "-o",
        "--outdir",
        dest="outdir",
        help="path to output directory (default: current working directory)",
    )
    parser.add_argument(
        "-c",
        "--cover-page",
        dest="cover",
        help="should the cover page be scanned for named entities to remove?",
        action="store_true",
    )
    parser.add_argument(
        "-r",
        "--regex",
        metavar="PATTERN",
        dest="patterns",
        nargs="*",
        help="one or more regex patterns to remove",
    )
    return parser


def get_person_entities(text: str) -> "list[str]":
    # todo: simple pre-trained model, ask Anna if she has ideas for a better one.
    out = set()
    for ent in nlp(text).ents:
        if (
            ent.label_ == "PERSON"
            and len(ent.text) >= 5
            # and len(ent.text.strip().split()) >= 2
        ):
            out.add(ent.text)
    return list(out)


def anonymize(text: str, actors: "list[str]" = [], patterns: "list[str]" = []):
    for entity in set(get_person_entities(text)):
        match = process.extractOne(entity, actors)
        if match and match[1] >= 90:
            id = actors.index(match[0])
            text = text.replace(entity, f"PERSON{id}")

    for id, actor in enumerate(actors):
        matches = find_near_matches(actor, text, max_l_dist=1)
        matches.reverse()
        for match in matches:
            text = __replace_substring(text, match.start, match.end, f"PERSON{id}")

    for id, pattern in enumerate(patterns):
        for match in compile(pattern).findall(text):
            text = text.replace(match, f"PATTERN{id}")

    return text


def __main():
    args = __init_argparse().parse_args()
    path = Path(args.file)

    content = extract_text(path)
    actors: list[str] = args.actors
    patterns: list[str] = args.patterns

    if args.cover:
        cover = extract_text(path, 0).split("intro")[0].split("Intro")[0]
        actors.extend(get_person_entities(cover))

    content = anonymize(content, actors, patterns)


def __replace_substring(
    string: str, start: int, end: int, replacement: str = ""
) -> str:
    return string[:start] + replacement + string[end:]


if __name__ == "__main__":
    __main()
