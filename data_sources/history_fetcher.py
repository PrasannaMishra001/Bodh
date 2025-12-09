import requests
from datetime import date
from bs4 import BeautifulSoup
from Bodh.config.settings import MAX_HISTORY_CHARS


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
        print(f"Error fetching history: {e}")
        return ""

    soup = BeautifulSoup(response.text, "html.parser")
    content_div = soup.find("span", {"id": "Events"})

    if not content_div:
        return ""

    ul = content_div.find_parent("h2").find_next_sibling("ul")
    if not ul:
        return ""

    items = ul.find_all("li")

    texts = []
    for item in items:
        texts.append(item.get_text(strip=True))

    combined = "\n".join(texts)

    if len(combined) > MAX_HISTORY_CHARS:
        combined = combined[:MAX_HISTORY_CHARS]

    return combined
