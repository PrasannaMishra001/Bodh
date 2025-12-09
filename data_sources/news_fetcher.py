from datetime import date
import feedparser
from bs4 import BeautifulSoup
from dateutil import parser as date_parser
from config.settings import MAX_NEWS_CHARS
from data_sources.rss_sources import RSS_FEEDS


def _clean_html(raw_html: str) -> str:
    soup = BeautifulSoup(raw_html, "html.parser")
    return soup.get_text(separator=" ", strip=True)


def fetch_news_for_date(target_date: date) -> str:
    """
    Fetch news headlines and summaries from the configured RSS feeds
    around the given date.

    This is a heuristic: many feeds do not allow exact date filtering,
    so we collect recent items and keep those close to target_date.
    """
    items = []

    for feed_url in RSS_FEEDS:
        try:
            feed = feedparser.parse(feed_url)
        except Exception as e:
            print(f"Error parsing feed {feed_url}: {e}")
            continue

        for entry in feed.entries:
            # Try to parse published date if available
            published = entry.get("published", "") or entry.get("updated", "")
            if not published:
                continue

            try:
                published_dt = date_parser.parse(published).date()
            except Exception:
                continue

            # Keep articles from the same date, or nearby (±1 day)
            if abs((published_dt - target_date).days) <= 1:
                title = entry.get("title", "")
                summary = entry.get("summary", "")
                text = f"{title}. {summary}"
                clean_text = _clean_html(text)
                items.append(clean_text)

    combined = "\n".join(items)
    if len(combined) > MAX_NEWS_CHARS:
        combined = combined[:MAX_NEWS_CHARS]

    return combined
