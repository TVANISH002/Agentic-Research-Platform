from __future__ import annotations

from core.state import ChunkRecord


def build_evidence_summary(chunks: list[ChunkRecord]) -> str:
    lines = []
    for chunk in chunks:
        preview = chunk.text[:280].replace("\n", " ")
        lines.append(f"[{chunk.source_id}] {chunk.title} | {chunk.url} | {preview}")
    return "\n".join(lines)
