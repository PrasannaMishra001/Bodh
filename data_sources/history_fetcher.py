import requests
from datetime import date
from bs4 import BeautifulSoup
from config.settings import MAX_HISTORY_CHARS


def fetch_history_for_date(target_date: date) -> str:
    month = target_date.strftime("%B")
    day = target_date.day

    url = f"https://en.wikipedia.org/wiki/{month}_{day}"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
    except Exception as e:
        print(f"Error fetching Wikipedia page: {e}")
        return ""

    soup = BeautifulSoup(response.text, "html.parser")

    headlines = soup.find_all("span", class_="mw-headline")

    target_span = None
    for span in headlines:
        if span.get_text(strip=True).lower() == "events":
            target_span = span
            break

    if not target_span:
        return ""

    ul = target_span.parent.find_next_sibling("ul")

    if not ul:
        return ""

    items = ul.find_all("li", recursive=False)

    texts = []
    for item in items:
        text = item.get_text(" ", strip=True)
        if text:
            texts.append(text)

    combined = "\n".join(texts)

    if len(combined) > MAX_HISTORY_CHARS:
        combined = combined[:MAX_HISTORY_CHARS]

    return combined
