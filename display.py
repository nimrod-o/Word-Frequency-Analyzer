BAR_WIDTH = 30  # max number of '#' characters in the longest bar


def bar_chart(count: int, max_count: int, width: int = BAR_WIDTH) -> str:

    if max_count <= 0:
        return ""
    length = round(count / max_count * width)
    return "#" * max(1, length)


def format_table(ranked: list[tuple[str, int]]) -> str:

    if not ranked:
        return ""

    max_count = ranked[0][1]
    # Word column is as wide as the longest word (but at least the header).
    word_width = max(len("Word"), max(len(word) for word, _ in ranked))
    count_width = max(len("Count"), len(str(max_count)))

    header = f"{'Rank':>4}  {'Word':<{word_width}}  {'Count':>{count_width}}  Chart"
    divider = f"{'-' * 4}  {'-' * word_width}  {'-' * count_width}  {'-' * BAR_WIDTH}"
    lines = [header, divider]

    for rank, (word, count) in enumerate(ranked, start=1):
        bar = bar_chart(count, max_count)
        lines.append(
            f"{rank:>4}  {word:<{word_width}}  {count:>{count_width}}  {bar}"
        )
    return "\n".join(lines)
