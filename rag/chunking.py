from __future__ import annotations

from core.config import settings
from core.state import ChunkRecord


def chunk_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    words = text.split()
    if not words:
        return []

    chunks: list[str] = []
    start = 0

    while start < len(words):
        end = min(len(words), start + chunk_size)
        chunk = " ".join(words[start:end])
        chunks.append(chunk)

        if end == len(words):
            break

        start = max(0, end - overlap)

    return chunks


def build_chunks(documents: list[dict]) -> list[ChunkRecord]:
    all_chunks: list[ChunkRecord] = []

    for doc in documents:
        text = doc.get("text", "")
        if not text:
            continue

        source_id = doc.get("source_id", "S0")
        title = doc.get("title", "Untitled")
        url = doc.get("url", "")

        raw_chunks = chunk_text(text, settings.chunk_size, settings.chunk_overlap)

        for idx, chunk in enumerate(raw_chunks, start=1):
            all_chunks.append(
                ChunkRecord(
                    chunk_id=f"{source_id}_C{idx}",
                    source_id=source_id,
                    title=title,
                    url=url,
                    text=chunk,
                )
            )

    return all_chunks