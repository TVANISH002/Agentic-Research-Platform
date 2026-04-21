from __future__ import annotations

from typing import Optional
import requests
from bs4 import BeautifulSoup
from core.config import settings


def scrape_url(url: str) -> Optional[str]:
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
        }

        response = requests.get(
            url,
            headers=headers,
            timeout=settings.request_timeout_seconds,
        )
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        for tag in soup(["script", "style", "nav", "footer", "header", "aside", "noscript"]):
            tag.decompose()

        text = soup.get_text(separator=" ", strip=True)
        text = " ".join(text.split())

        if not text:
            return None

        return text[: settings.max_chars_per_doc]

    except Exception:
        return None


def scrape_many(results: list[dict]) -> list[dict]:
    """
    Accepts Tavily-style search results and returns successfully scraped documents.

    Expected input item shape:
    {
        "title": "...",
        "url": "...",
        "content": "..."
    }
    """
    documents = []

    for i, item in enumerate(results[: settings.max_urls_to_scrape], start=1):
        url = item.get("url", "")
        if not url:
            continue

        scraped_text = scrape_url(url)
        if not scraped_text:
            continue

        documents.append(
            {
                "source_id": f"S{i}",
                "title": item.get("title", "Untitled"),
                "url": url,
                "snippet": item.get("content", ""),
                "text": scraped_text,
            }
        )

    return documents