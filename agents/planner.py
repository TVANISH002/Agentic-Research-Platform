# from __future__ import annotations

# from core.llm import chat_json

# PLANNER_SYSTEM = """
# You are a research planning agent. Break broad topics into high-quality web research subqueries.
# Return valid JSON only.
# """.strip()


# def plan_queries(topic: str) -> list[str]:
#     prompt = f"""
# Topic: {topic}

# Create 4 concise web research queries that together help answer this topic thoroughly.
# The queries should cover:
# 1. current overview
# 2. technical details
# 3. recent developments or benchmarks
# 4. risks, limitations, or business impact

# Return JSON in this exact schema:
# {{"queries": ["...", "...", "...", "..."]}}
# """.strip()
#     data = chat_json(PLANNER_SYSTEM, prompt)
#     queries = data.get("queries", [])
#     return [q.strip() for q in queries if isinstance(q, str) and q.strip()]



from __future__ import annotations
from typing import List, Dict
from core.llm import chat_json

PLANNER_SYSTEM = """
You are a research planning agent.

Return ONLY valid JSON.
Generate 4–6 diverse web search queries.
Each query must target a different aspect:
- overview
- technical
- recent updates
- risks/limitations
""".strip()


def plan_queries(topic: str) -> List[Dict[str, str]]:
    prompt = f"""
Topic: {topic}

Return JSON:
{{
  "queries": [
    {{"query": "...", "type": "overview"}},
    {{"query": "...", "type": "technical"}},
    {{"query": "...", "type": "recent"}},
    {{"query": "...", "type": "risks"}}
  ]
}}
""".strip()

    data = chat_json(PLANNER_SYSTEM, prompt)

    queries = data.get("queries", [])

    # HARD GUARANTEE: always return list of dicts
    safe_queries = []

    if isinstance(queries, list):
        for q in queries:
            if isinstance(q, dict) and "query" in q:
                safe_queries.append({
                    "query": str(q["query"]).strip(),
                    "type": str(q.get("type", "unknown")).strip()
                })

    return safe_queries