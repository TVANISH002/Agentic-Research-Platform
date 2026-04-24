from __future__ import annotations

from core.state import ChunkRecord


def build_evidence_summary(chunks: list[ChunkRecord], preview_chars: int = 280) -> str:
    if not chunks:
        return "No evidence chunks available."

    lines = []

    for i, chunk in enumerate(chunks, start=1):
        preview = chunk.text.replace("\n", " ").strip()
        if len(preview) > preview_chars:
            preview = preview[:preview_chars].rstrip() + "..."

        lines.append(
            f"Evidence {i}\n"
            f"- Chunk ID: {chunk.chunk_id}\n"
            f"- Source ID: {chunk.source_id}\n"
            f"- Title: {chunk.title}\n"
            f"- URL: {chunk.url}\n"
            f"- Preview: {preview}"
        )

    return "\n\n".join(lines)