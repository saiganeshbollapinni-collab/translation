# translation

A small command-line tool for translating text between languages, built on
[`deep-translator`](https://pypi.org/project/deep-translator/) (no API key needed).

## Setup

```bash
pip install -r requirements.txt
```

## Usage

```bash
# English -> Telugu
python translate.py "Hello, how are you?" --to te

# Telugu -> English (explicit source language)
python translate.py "నమస్కారం" --from te --to en

# Translate a file and save the result
python translate.py --file notes.txt --to hi --out notes_hi.txt

# Read from stdin
echo "Good morning" | python translate.py --to te

# See supported language codes
python translate.py --list-languages
```

The source language is auto-detected unless you pass `--from`. The default
target is English (`en`).

## Notes

- Long text is split into chunks automatically to stay under the free
  endpoint's size limit.
- An internet connection is required.
