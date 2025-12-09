import requests
from datetime import date
from bs4 import BeautifulSoup
from config.settings import MAX_HISTORY_CHARS


def fetch_history_for_date(target_date: date) -> str:
    """
    Fetch 'On This Day' style history events from Wikipedia REST API.

    This uses:
    https://en.wikipedia.org/api/rest_v1/feed/onthisday/events/{month}/{day}
    """
    month = target_date.month
    day = target_date.day

    url = f"https://en.wikipedia.org/api/rest_v1/feed/onthisday/events/{month}/{day}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"Error fetching history: {e}")
        return ""

    data = response.json()
    events = data.get("events", [])

    texts = []
    for event in events:
        year = event.get("year", "")
        pages = event.get("pages", [])
        description = event.get("text", "")

        title = pages[0]["titles"]["normalized"] if pages else ""
        line = f"{year}: {description} ({title})"
        texts.append(line)

    combined = "\n".join(texts)
    if len(combined) > MAX_HISTORY_CHARS:
        combined = combined[:MAX_HISTORY_CHARS]

    return combined
