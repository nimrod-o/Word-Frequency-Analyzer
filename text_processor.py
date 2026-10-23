"""Pure text-processing functions: clean, tokenize, remove stopwords.

DESIGN NOTE: every function in this module is *pure*. It takes a value in and
returns a new value out, with no printing, no file access, and no changes to
its arguments. That makes each function trivial to unit test on its own
(``assert tokenize("Hi, hi!") == ["hi", "hi"]``) without creating files or
capturing terminal output. All I/O lives in analyzer.py instead.
"""

import re


def clean_text(text: str) -> str:
    """Lowercase the text and replace punctuation with spaces.

    Judgment calls (documented, as the project brief asks):

    * Apostrophes are KEPT so "don't" stays "don't" instead of becoming the
      meaningless "dont". Curly apostrophes (') are normalised to straight
      ones first, since real-world text is full of them.
    * Single hyphens are KEPT so "well-known" stays one word. It's a
      judgment call: splitting would give "well" and "known", but the
      compound usually carries its own meaning. Double hyphens ("--", often
      used as a dash) are treated as separators.
    * Everything else that is not a letter, digit, or whitespace becomes a
      space (not an empty string!) so "end.Start" becomes "end start"
      rather than gluing two words into "endstart".
    * Windows ("\\r\\n") and Unix ("\\n") line endings, tabs and repeated
      spaces are all whitespace, so collapsing whitespace handles them.

    Args:
        text: Raw text, possibly multi-line.

    Returns:
        Lowercase text with single spaces between chunks.
    """
    text = text.lower()
    text = text.replace("\u2019", "'").replace("\u2018", "'")  # curly quotes
    text = re.sub(r"-{2,}", " ", text)          # "--" acts as a separator
    text = re.sub(r"[^\w\s'-]", " ", text)      # drop other punctuation
    text = text.replace("_", " ")               # \w includes underscores
    return re.sub(r"\s+", " ", text).strip()    # collapse all whitespace


def tokenize(text: str, min_length: int = 1) -> list[str]:
    """Split cleaned text into a list of word tokens.

    Number handling: tokens made ONLY of digits ("2025", "3", "000") are
    dropped. A number on its own rarely tells you what a text is about, and
    it would clutter the ranking. Mixed tokens like "4th" or "3g" are kept
    because they are word-like. (Note "3,000" becomes "3" and "000" during
    cleaning, so both pieces are dropped too.)

    Args:
        text: Text that has already been through clean_text().
        min_length: Discard tokens shorter than this many characters. This
            removes noise such as the stray "s" left over from odd
            punctuation.

    Returns:
        List of tokens in their original order (duplicates preserved).
    """
    tokens: list[str] = []
    for raw in text.split():
        # Strip apostrophes/hyphens hanging off the edges: 'hello' -> hello
        token = raw.strip("'-")
        if not token or token.isdigit():
            continue
        if len(token) >= min_length:
            tokens.append(token)
    return tokens


def remove_stopwords(tokens: list[str], stopwords: set[str]) -> list[str]:
    """Return only the tokens that are not in the stopword set.

    Args:
        tokens: Lowercase tokens.
        stopwords: Set of words to exclude.

    Returns:
        A new list; the input list is left untouched.
    """
    return [token for token in tokens if token not in stopwords]
