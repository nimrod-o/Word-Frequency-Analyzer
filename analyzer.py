import argparse
import sys
from pathlib import Path

from display import format_table
from frequency import count_words, get_top_n
from stopwords import ENGLISH_STOPWORDS, SWAHILI_STOPWORDS
from text_processor import clean_text, remove_stopwords, tokenize


def positive_int(value: str) -> int:
    try:
        number = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"'{value}' is not a whole number")
    if number < 1:
        raise argparse.ArgumentTypeError("value must be 1 or greater")
    return number


def build_parser() -> argparse.ArgumentParser:
   
    parser = argparse.ArgumentParser(
        description="Count the most common words in a text file."
    )
    parser.add_argument("--file", required=True, help="path to the .txt file to analyze")
    parser.add_argument("--top", type=positive_int, default=10,
                        help="how many top words to show (default: 10)")
    parser.add_argument("--lang", choices=["en", "sw", "both"], default="en",
                        help="stopword language: en, sw, or both (default: en)")
    parser.add_argument("--min-length", type=positive_int, default=3,
                        help="ignore words shorter than this (default: 3)")
    return parser


def read_text_file(path: Path) -> str:
    
    with open(path, "r", encoding="utf-8-sig") as handle:
        return handle.read()


def select_stopwords(lang: str) -> set[str]:

    if lang == "en":
        return ENGLISH_STOPWORDS
    if lang == "sw":
        return SWAHILI_STOPWORDS
    return ENGLISH_STOPWORDS | SWAHILI_STOPWORDS  # union of both sets


def main(argv: list[str] | None = None) -> int:

    args = build_parser().parse_args(argv)
    path = Path(args.file)

    try:
        text = read_text_file(path)
    except FileNotFoundError:
        print(f"Error: file not found: {path}", file=sys.stderr)
        return 1
    except IsADirectoryError:
        print(f"Error: '{path}' is a folder, not a text file.", file=sys.stderr)
        return 1
    except PermissionError:
        print(f"Error: no permission to read '{path}'.", file=sys.stderr)
        return 1
    except UnicodeDecodeError:
        print(f"Error: '{path}' is not valid UTF-8 text. Re-save it with "
              "UTF-8 encoding and try again.", file=sys.stderr)
        return 1

    tokens = tokenize(clean_text(text), min_length=args.min_length)
    words = remove_stopwords(tokens, select_stopwords(args.lang))

    if not words:
        print("No words found in this file.")
        return 0

    counts = count_words(words)
    top = get_top_n(counts, args.top)

    print(f"File: {path}  |  language: {args.lang}  |  min length: {args.min_length}")
    print(f"{len(words)} words counted, {len(counts)} distinct. "
          f"Showing top {len(top)}:\n")
    print(format_table(top))
    return 0


if __name__ == "__main__":
    sys.exit(main())
