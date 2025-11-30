import re
from collections import Counter


def extract_keywords(text: str, top_k: int = 5):
    words = re.findall(r"\w+", text.lower())
    stopwords = set(["the", "and", "is", "in", "to", "of", "a", "for", "on", "with", "that", "are"])
    filtered = [w for w in words if w not in stopwords and len(w) > 2]
    counts = Counter(filtered)
    return [k for k, _ in counts.most_common(top_k)]
