from __future__ import annotations

import os
from pathlib import Path
from typing import List, Dict
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed

from dotenv import load_dotenv
from tavily import TavilyClient
from core.config import settings

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)


def _dedupe_results(results: List[Dict]) -> List[Dict]:
    seen_urls = set()
    unique = []

    for r in results:
        url = r.get("url")
        if url and url not in seen_urls:
            seen_urls.add(url)
            unique.append(r)

    return unique


def _score_result(result: Dict) -> float:
    score = 0.0
    content = result.get("content", "") or ""
    title = result.get("title", "") or ""

    score += min(len(content) / 1000, 2)
    score += min(len(title) / 50, 1)
    return score


def _search_one(client: TavilyClient, q: Dict[str, str]) -> List[Dict]:
    query_text = q.get("query")
    if not query_text:
        return []

    response = client.search(
        query=query_text,
        max_results=settings.max_search_results,
        search_depth="advanced",
    )

    results = response.get("results", [])
    for r in results:
        r["query_type"] = q.get("type", "unknown")
    return results


def run_web_search(queries: List[Dict[str, str]]) -> List[Dict]:
    tavily_key = settings.tavily_api_key or os.getenv("TAVILY_API_KEY")
    if not tavily_key:
        raise ValueError("TAVILY_API_KEY missing")

    client = TavilyClient(api_key=tavily_key)
    all_results: List[Dict] = []

    with ThreadPoolExecutor(max_workers=min(4, len(queries))) as executor:
        futures = [executor.submit(_search_one, client, q) for q in queries]

        for future in as_completed(futures):
            try:
                all_results.extend(future.result())
            except Exception:
                continue

    all_results = _dedupe_results(all_results)
    all_results.sort(key=_score_result, reverse=True)
    return all_results[: settings.max_total_results]