# Word Frequency Analyzer

A command-line tool that reads a text file and prints the most common words as a ranked table with a `#` bar chart. Standard library only, Python 3.10+.

Built as **Project 2** of my Python Rebuild Week (Day 1: strings, dictionaries, sorting, file I/O).

## What it does

1. Reads a `.txt` file (UTF-8)
2. Cleans it: lowercases, strips punctuation, keeps contractions (`don't`) and hyphenated words (`well-known`)
3. Tokenizes into words, dropping pure numbers and words shorter than `--min-length`
4. Removes stopwords (English, Swahili, or both) using hand-built Python sets
5. Counts with `collections.Counter` and prints the top N

## How to run

```bash
python analyzer.py --file sample_article.txt
python analyzer.py --file sample_article.txt --top 20
python analyzer.py --file sample_mixed.txt --lang both
python analyzer.py --file notes.txt --min-length 4
```

| Flag | Required | Default | Meaning |
|---|---|---|---|
| `--file` | yes | | Path to the text file |
| `--top` | no | 10 | How many words to show |
| `--lang` | no | `en` | `en`, `sw`, or `both` stopword sets |
| `--min-length` | no | 3 | Ignore words shorter than this |

## Example output

```
$ python analyzer.py --file sample_article.txt

File: sample_article.txt  |  language: en  |  min length: 3
175 words counted, 146 distinct. Showing top 10:

Rank  Word       Count  Chart
----  ---------  -----  ------------------------------
   1  training       5  ##############################
   2  courses        4  ########################
   3  centres        3  ##################
   4  employers      3  ##################
   5  nakuru         3  ##################
   6  say            3  ##################
   7  skills         3  ##################
   8  students       3  ##################
   9  digital        2  ############
  10  education      2  ############
```

Mixed Swahili/English:

```
$ python analyzer.py --file sample_mixed.txt --lang both --top 8

Rank  Word       Count  Chart
----  ---------  -----  ------------------------------
   1  kujifunza      3  ##############################
   2  students       3  ##############################
   3  computer       2  ####################
   4  jinsi          2  ####################
   5  kubwa          2  ####################
   6  mpya           2  ####################
   7  mwezi          2  ####################
   8  skills         2  ####################
```

## Files

| File | Job |
|---|---|
| `analyzer.py` | Entry point: argparse, file reading, error handling, runs the pipeline |
| `text_processor.py` | Pure functions: `clean_text`, `tokenize`, `remove_stopwords` |
| `stopwords.py` | `ENGLISH_STOPWORDS` and `SWAHILI_STOPWORDS` sets |
| `frequency.py` | `count_words`, `get_top_n` |
| `display.py` | `format_table`, `bar_chart` |

## Design decisions

- **Language handling:** I used an explicit `--lang en|sw|both` flag instead of per-word auto-detection. Short words are ambiguous between languages, so a heuristic would guess wrong quietly. With `both`, the two stopword sets are merged with a set union.
- **Numbers are dropped**, since a bare `2025` says nothing about a text's topic.
- **Contractions and hyphenated words are kept whole**, so the stopword sets include contractions like `don't`.
- **Ties are sorted alphabetically**, so output is the same every run.

## Error handling

Missing file, folder instead of file, permission error, non-UTF-8 file, empty file (or one with only stopwords), and invalid `--top` / `--min-length` values all give a clear message with no traceback.

## What I learned

- Splitting a program into small pure functions made each step easy to reason about and to test in isolation. Keeping all file access in `analyzer.py` is what makes that possible.
- Cleaning text is mostly judgment calls (apostrophes, hyphens, numbers). Deciding and documenting them mattered more than the regex itself.
- Punctuation should be replaced with a space, not deleted, or `end.Start` glues into `endstart`.
- `Counter.most_common` doesn't order ties deterministically in a useful way, so I sort by `(-count, word)` myself.
- Sets make stopword lookup fast, and `set | set` is a neat way to combine languages.
- Swahili stopwords only catch standalone words. Grammar attached inside long verbs (`ninaenda`) slips through, which would need stemming, a good next step.
- Using `utf-8-sig` handles the invisible BOM that Windows Notepad adds.
