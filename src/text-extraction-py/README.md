# Extract, Anonymize, Complement

A wrapper package for performing a set of common text analyses tasks;

- extract text from documents (e.g., `.docx`, `.pdf`, and other standard formats)
- remove personal details from texts (e.g., names, dates, and with patterns; email addresses, student numbers, etc.)
- isolate new or changed content from several iterations of the same document

## Installation

We encourage the use of virtual environments. Before installing this package, consider creating a new virtual environment using your choice of conda, venv, pipenv, virtualenv, etc.

This package is not listed on `PyPI`, but can be installed directly from github;

```bash
pip install "git+https://github.com/BDSI-Utwente/mariana-conceptual-networks.git#egg=eac_py&subdirectory=src/text-extraction-py"
```

You will also need to download the spaCy model used;

```bash
python -m spacy download en_core_web_md
```

## Usage

```py
from eac_py.extract import extract_text
from eac_py.anonymize import anonymize_known_persons
from eac_py.complement import complement

persons = ["John Doe", "Jane Baker", "S. Ome-Person"]

text = extract_text("../path/to/file.pdf")
text_anonymized = anonymize_known_persons(text, persons)
text_v2 = extract_text("../path/to/file v2.pdf")
text_v2_anonymized = anonymize_known_persons(text_v2, persons)
new_text = complement(text, text_v2)
```
