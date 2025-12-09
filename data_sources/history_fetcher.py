import requests
from datetime import date
from config.settings import MAX_HISTORY_CHARS


def fetch_history_for_date(target_date: date) -> str:
    month = target_date.month
    day = target_date.day

    url = f"https://byabbe.se/on-this-day/{month}/{day}/events.json"

    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
    except Exception as e:
        print(f"Error fetching history: {e}")
        return ""

    data = response.json()
    events = data.get("events", [])

    texts = []
    for event in events:
        year = event.get("year", "")
        description = event.get("description", "")
        line = f"{year}: {description}"
        texts.append(line)

    combined = "\n".join(texts)

    if len(combined) > MAX_HISTORY_CHARS:
        combined = combined[:MAX_HISTORY_CHARS]

    return combined
