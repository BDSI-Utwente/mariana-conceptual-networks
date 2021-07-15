from typing import Union
import spacy
from fuzzywuzzy import process
from fuzzysearch import find_near_matches
from re import compile

nlp = spacy.load("en_core_web_md")


def get_person_entities(text: str) -> list[str]:
    # todo: simple pre-trained model, ask Anna if she has ideas for a better one.
    out = set()
    for ent in nlp(text).ents:
        if ent.label_ == "PERSON" and len(ent.text) >= 5:
            out.add(ent.text)
    return list(out)


def anonymize_dates(text: str, replace: bool = False) -> str:
    dates = [
        date.text
        for date in nlp(text).ents
        if (date.label_ == "DATE" or date.label_ == "TIME") and len(date.text) > 4
    ]
    for id, date in enumerate(dates):
        if replace:
            text = text.replace(date, f"DATE{id}")
        else:
            text = text.replace(date, "")
    return text


def anonymize_unknown_persons(text: str, replace: bool = False) -> str:
    persons = get_person_entities(text)
    return anonymize_known_persons(text, persons, replace)


def anonymize_patterns(
    text: str, patterns: list[str], replace: Union[list[str], bool] = False
) -> str:
    for id, pattern in enumerate(patterns):
        for match in compile(pattern).findall(text):
            if replace:
                if isinstance(replace, list):
                    text = text.replace(match, replace[id])
                else:
                    text = text.replace(match, f"PATTERN{id}")
            else:
                text = text.replace(match, "")
    return text


def anonymize_known_persons(
    text: str, persons: list[str], replace: Union[bool, list[str]] = False
) -> str:

    for entity in set(get_person_entities(text)):
        match = process.extractOne(entity, persons)
        if match and match[1] >= 90:
            if replace:
                id = persons.index(match[0])
                if isinstance(replace, list):
                    text = text.replace(entity, list[id])
                else:
                    text = text.replace(entity, f"PERSON{id}")
            else:
                text = text.replace(entity, "")

    for id, person in enumerate(persons):
        matches = find_near_matches(person, text, max_l_dist=1)
        matches.reverse()
        for match in matches:
            if replace:
                if isinstance(replace, list):
                    text = __replace_substring(
                        text, match.start, match.end, replace[id]
                    )
                else:
                    text = __replace_substring(
                        text, match.start, match.end, f"PERSON{id}"
                    )
            else:
                text = __replace_substring(text, match.start, match.end, "")

    return text


def __replace_substring(
    string: str, start: int, end: int, replacement: str = ""
) -> str:
    return string[:start] + replacement + string[end:]
