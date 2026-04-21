from __future__ import annotations

from core.llm import chat_json

PLANNER_SYSTEM = """
You are a research planning agent. Break broad topics into high-quality web research subqueries.
Return valid JSON only.
""".strip()


def plan_queries(topic: str) -> list[str]:
    prompt = f"""
Topic: {topic}

Create 4 concise web research queries that together help answer this topic thoroughly.
The queries should cover:
1. current overview
2. technical details
3. recent developments or benchmarks
4. risks, limitations, or business impact

Return JSON in this exact schema:
{{"queries": ["...", "...", "...", "..."]}}
""".strip()
    data = chat_json(PLANNER_SYSTEM, prompt)
    queries = data.get("queries", [])
    return [q.strip() for q in queries if isinstance(q, str) and q.strip()]
