from utils.text_cleaner import normalize_whitespace


def format_quiz_markdown(quiz_text: str) -> str:
    """
    Prepare quiz text for display in Streamlit markdown.
    Currently this just normalizes whitespace.
    """
    return normalize_whitespace(quiz_text or "")
