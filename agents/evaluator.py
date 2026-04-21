from __future__ import annotations

from core.llm import chat_json
from core.state import EvaluationResult

EVAL_SYSTEM = """
You are a strict research report evaluator.
Judge only based on the provided report and evidence summary.
Return JSON only.
""".strip()


def evaluate_report(topic: str, report: str, evidence_summary: str) -> EvaluationResult:
    prompt = f"""
Topic: {topic}

Evidence summary:
{evidence_summary}

Report:
{report}

Evaluate the report on a scale of 1 to 10 for:
- relevance
- grounding
- completeness
- clarity
- citation_coverage

Return JSON with this exact schema:
{{
  "overall_score": 0,
  "relevance": 0,
  "grounding": 0,
  "completeness": 0,
  "clarity": 0,
  "citation_coverage": 0,
  "strengths": ["..."],
  "weaknesses": ["..."],
  "verdict": "..."
}}
""".strip()
    data = chat_json(EVAL_SYSTEM, prompt)
    return EvaluationResult(
        overall_score=float(data.get("overall_score", 0)),
        relevance=float(data.get("relevance", 0)),
        grounding=float(data.get("grounding", 0)),
        completeness=float(data.get("completeness", 0)),
        clarity=float(data.get("clarity", 0)),
        citation_coverage=float(data.get("citation_coverage", 0)),
        strengths=list(data.get("strengths", [])),
        weaknesses=list(data.get("weaknesses", [])),
        verdict=str(data.get("verdict", "")),
    )
