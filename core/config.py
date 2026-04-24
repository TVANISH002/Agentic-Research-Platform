from __future__ import annotations

import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    groq_api_key: str = os.getenv("GROQ_API_KEY", "")
    tavily_api_key: str = os.getenv("TAVILY_API_KEY", "")
    groq_base_url: str = os.getenv("GROQ_BASE_URL", "https://api.groq.com/openai/v1")
    groq_model: str = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    max_search_results: int = int(os.getenv("MAX_SEARCH_RESULTS", "6"))
    max_total_results: int = int(os.getenv("MAX_TOTAL_RESULTS", "9"))
    max_urls_to_scrape: int = int(os.getenv("MAX_URLS_TO_SCRAPE", "4"))
    max_chars_per_doc: int = int(os.getenv("MAX_CHARS_PER_DOC", "12000"))
    chunk_size: int = int(os.getenv("CHUNK_SIZE", "855"))
    chunk_overlap: int = int(os.getenv("CHUNK_OVERLAP", "130"))
    top_k_chunks: int = int(os.getenv("TOP_K_CHUNKS", "6"))
    evaluation_threshold: float = float(os.getenv("EVALUATION_THRESHOLD", "7.8"))
    request_timeout_seconds: int = int(os.getenv("REQUEST_TIMEOUT_SECONDS", "20"))



    


settings = Settings()