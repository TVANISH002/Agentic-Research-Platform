from __future__ import annotations

from core.llm import chat_completion
from core.state import ChunkRecord

WRITER_SYSTEM = """
You are an expert research writer.
Write grounded, professional, factual reports using only the supplied evidence.
Every important factual claim must use source tags like [S1], [S2].
Do not invent citations.
""".strip()


def format_evidence(chunks: list[ChunkRecord]) -> str:
    blocks = []
    for chunk in chunks:
        blocks.append(
            f"[{chunk.source_id}] Title: {chunk.title}\nURL: {chunk.url}\nEvidence: {chunk.text}"
        )
    return "\n\n".join(blocks)


def write_report(topic: str, chunks: list[ChunkRecord], planned_queries: list[str]) -> str:
    evidence = format_evidence(chunks)
    user_prompt = f"""
Topic: {topic}

Planned research angles:
{chr(10).join(f'- {q}' for q in planned_queries)}

Evidence:
{evidence}

Write a structured report with these sections:
1. Executive Summary
2. Key Findings
3. Technical Details
4. Risks / Limitations
5. Conclusion
6. Sources

Rules:
- Use only evidence provided.
- Use inline source tags like [S1] or [S2] for factual claims.
- In Sources, list each source_id with its URL once.
- Keep the writing detailed but concise.
""".strip()
    return chat_completion(WRITER_SYSTEM, user_prompt, temperature=0.2)


def rewrite_report(topic: str, report: str, weaknesses: list[str], chunks: list[ChunkRecord]) -> str:
    evidence = format_evidence(chunks)
    weak_text = "\n".join(f"- {w}" for w in weaknesses) if weaknesses else "- Improve grounding and completeness"
    user_prompt = f"""
Topic: {topic}

Current report:
{report}

Weaknesses to fix:
{weak_text}

Available evidence:
{evidence}

Rewrite the report to improve grounding, completeness, and citation quality.
Use the same report structure and cite with [S1]-style markers.
""".strip()
    return chat_completion(WRITER_SYSTEM, user_prompt, temperature=0.2)
