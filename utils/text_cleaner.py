import re


def normalize_whitespace(text: str) -> str:
    """
    Replace multiple spaces and newlines with single spaced clean text.
    """
    if not text:
        return ""
    text = re.sub(r"\s+", " ", text)
    return text.strip()
