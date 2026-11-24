#!/usr/bin/env python3
"""Simple command-line text translator.

Examples:
    python translate.py "Hello, how are you?" --to te
    python translate.py "నమస్కారం" --from te --to en
    python translate.py --file notes.txt --to hi --out notes_hi.txt
    echo "Good morning" | python translate.py --to te
    python translate.py --list-languages
"""
import argparse
import sys

from deep_translator import GoogleTranslator

MAX_CHUNK = 4500  # Google's free endpoint limits requests to ~5000 characters


def chunk_text(text: str, size: int = MAX_CHUNK):
    """Split text on line boundaries into chunks no longer than `size`."""
    chunks, current = [], ""
    for line in text.splitlines(keepends=True):
        while len(line) > size:  # a single very long line
            if current:
                chunks.append(current)
                current = ""
            chunks.append(line[:size])
            line = line[size:]
        if len(current) + len(line) > size:
            chunks.append(current)
            current = ""
        current += line
    if current:
        chunks.append(current)
    return chunks


def translate(text: str, source: str, target: str) -> str:
    translator = GoogleTranslator(source=source, target=target)
    parts = []
    for chunk in chunk_text(text):
        if chunk.strip():
            parts.append(translator.translate(chunk))
        else:
            parts.append(chunk)
    return "".join(parts)


def main() -> int:
    parser = argparse.ArgumentParser(description="Translate text between languages.")
    parser.add_argument("text", nargs="?", help="Text to translate (or use --file / stdin)")
    parser.add_argument("--file", "-f", help="Read text from this file")
    parser.add_argument("--out", "-o", help="Write the result to this file")
    parser.add_argument("--from", dest="source", default="auto",
                        help="Source language code (default: auto-detect)")
    parser.add_argument("--to", dest="target", default="en",
                        help="Target language code (default: en)")
    parser.add_argument("--list-languages", action="store_true",
                        help="Show supported language codes and exit")
    args = parser.parse_args()

    if args.list_languages:
        langs = GoogleTranslator().get_supported_languages(as_dict=True)
        for name, code in sorted(langs.items()):
            print(f"{code:8} {name}")
        return 0

    if args.file:
        with open(args.file, encoding="utf-8") as fh:
            text = fh.read()
    elif args.text:
        text = args.text
    elif not sys.stdin.isatty():
        text = sys.stdin.read()
    else:
        parser.print_help()
        return 1

    try:
        result = translate(text, args.source, args.target)
    except Exception as exc:  # network errors, bad language codes, etc.
        print(f"Translation failed: {exc}", file=sys.stderr)
        return 2

    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(result)
        print(f"Saved translation to {args.out}")
    else:
        print(result)
    return 0


if __name__ == "__main__":
    sys.exit(main())
