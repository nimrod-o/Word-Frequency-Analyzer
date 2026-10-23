"""Counting words and ranking them."""

from collections import Counter


def count_words(words: list[str]) -> Counter[str]:
    """Count how many times each word appears.

    Args:
        words: List of tokens (duplicates expected).

    Returns:
        A Counter mapping each distinct word to its count.
    """
    return Counter(words)


def get_top_n(counts: Counter[str], n: int) -> list[tuple[str, int]]:
    """Return the n most frequent words as (word, count) tuples.

    Sorted by count (highest first). Ties are broken alphabetically so the
    output is identical on every run, which makes results easy to compare
    and test. If n is larger than the number of distinct words, we simply
    return all of them; slicing never pads or raises an error.

    Args:
        counts: Counter produced by count_words().
        n: How many entries to return.

    Returns:
        List of (word, count) tuples, most frequent first.
    """
    ranked = sorted(counts.items(), key=lambda pair: (-pair[1], pair[0]))
    return ranked[:n]
