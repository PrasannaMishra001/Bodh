import requests
from datetime import date
from bs4 import BeautifulSoup
from config.settings import MAX_HISTORY_CHARS


def fetch_history_for_date(target_date: date) -> str:
    """
    Scrapes Wikipedia's 'On This Day' page for historical events.
    """
    month = target_date.month
    day = target_date.day
    
    months = [
        "", "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    month_name = months[month]
    
    url = f"https://en.wikipedia.org/wiki/{month_name}_{day}"
    
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
    except Exception as e:
        print(f"Error fetching Wikipedia page: {e}")
        return ""
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    events_section = None
    for heading in soup.find_all(['h2', 'h3']):
        if 'Events' in heading.get_text():
            events_section = heading
            break
    
    if not events_section:
        print("Could not find Events section on Wikipedia page")
        return ""
    
    texts = []
    current = events_section.find_next_sibling()
    
    while current and current.name != 'h2':
        if current.name == 'ul':
            for li in current.find_all('li', recursive=False):
                text = li.get_text(separator=' ', strip=True)
                if text:
                    texts.append(text)
        current = current.find_next_sibling()
    
    combined = "\n".join(texts)
    
    if len(combined) > MAX_HISTORY_CHARS:
        combined = combined[:MAX_HISTORY_CHARS]
    
    return combined
