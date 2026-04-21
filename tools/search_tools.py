from __future__ import annotations

import os
from pathlib import Path
from dotenv import load_dotenv
from tavily import TavilyClient
from core.config import settings

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)


def run_web_search(query: str) -> list[dict]:
    tavily_key = settings.tavily_api_key or os.getenv("TAVILY_API_KEY")

    if not tavily_key:
        raise ValueError("TAVILY_API_KEY missing")

    client = TavilyClient(api_key=tavily_key)

    response = client.search(
        query=query,
        max_results=settings.max_search_results,
        search_depth="advanced",
    )

    return response.get("results", [])