"""Stopword lists for the Word Frequency Analyzer.

Stopwords are very common "glue" words (the, and, of ...) that would
otherwise dominate every frequency table without telling us anything about
what the text is actually about.

They are stored as Python sets (not lists) because membership tests such as
``word in ENGLISH_STOPWORDS`` are O(1) on a set but O(n) on a list. With
thousands of words to check, that difference adds up.
"""

# Contractions are included on purpose: our tokenizer keeps "don't" as one
# token (see text_processor.py), so the stopword list must contain it too.
ENGLISH_STOPWORDS: set[str] = {
    "a", "about", "above", "after", "again", "all", "also", "am", "an", "and",
    "any", "are", "as", "at", "be", "because", "been", "before", "being",
    "below", "between", "both", "but", "by", "can", "could", "did", "do",
    "does", "doing", "down", "during", "each", "few", "for", "from",
    "further", "had", "has", "have", "having", "he", "her", "here", "hers",
    "him", "his", "how", "i", "if", "in", "into", "is", "it", "its", "just",
    "me", "more", "most", "my", "no", "nor", "not", "now", "of", "off", "on",
    "once", "only", "or", "other", "our", "ours", "out", "over", "own",
    "said", "same", "she", "should", "so", "some", "such", "than", "that",
    "the", "their", "theirs", "them", "then", "there", "these", "they",
    "this", "those", "through", "to", "too", "under", "until", "up", "very",
    "was", "we", "were", "what", "when", "where", "which", "while", "who",
    "whom", "why", "will", "with", "would", "you", "your", "yours",
    # Contractions
    "don't", "doesn't", "didn't", "isn't", "aren't", "wasn't", "weren't",
    "hasn't", "haven't", "hadn't", "won't", "wouldn't", "can't", "couldn't",
    "shouldn't", "it's", "i'm", "i've", "i'll", "i'd", "you're", "you've",
    "you'll", "he's", "she's", "we're", "we've", "they're", "they've",
    "that's", "there's", "what's", "let's",
}

# Swahili is agglutinative: many grammatical ideas are attached to verbs as
# prefixes (e.g. "ninaenda" = ni-na-enda, "I am going"). A simple stopword
# set can only catch the *standalone* function words below, not those
# embedded inside longer verbs. That's a known limitation of this approach.
SWAHILI_STOPWORDS: set[str] = {
    # Connectors and prepositions
    "na", "ya", "wa", "kwa", "la", "za", "cha", "vya", "pa", "kwenye",
    "katika", "kutoka", "hadi", "mpaka", "baada", "kabla", "wakati", "kisha",
    "tena", "pia", "au", "ama", "lakini", "ila", "kama", "kwamba", "ingawa",
    "ili", "hata", "kwani", "basi", "ndiyo", "ndio", "hapana",
    # "To be" / "to have" / existence
    "ni", "si", "siyo", "sio", "kuwa", "alikuwa", "walikuwa", "ilikuwa",
    "atakuwa", "ana", "una", "nina", "tuna", "wana", "ina", "kuna", "hakuna",
    # Demonstratives and relatives
    "hii", "hiyo", "huu", "huo", "hili", "hilo", "hizi", "hizo", "haya",
    "hayo", "ile", "ule", "lile", "yale", "zile", "hawa", "wale",
    "ambaye", "ambao", "ambayo", "ambazo", "ambalo", "ambacho",
    # Pronouns and possessives
    "mimi", "wewe", "yeye", "sisi", "nyinyi", "wao", "yangu", "yako", "yake",
    "yetu", "yenu", "yao", "wangu", "wako", "wake", "wetu", "wenu", "zao",
    "changu", "chako", "chake", "chao",
    # Common small adverbs / quantifiers
    "hapa", "hapo", "pale", "huko", "sasa", "bado", "tu", "sana", "kila",
    "wote", "yote", "zote", "vyote", "lote", "kabisa", "hasa", "kidogo",
}
