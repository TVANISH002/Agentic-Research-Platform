from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class SourceDocument:
    source_id: str
    title: str
    url: str
    snippet: str
    content: str
    domain: str
    search_score: float | None = None


@dataclass
class ChunkRecord:
    chunk_id: str
    source_id: str
    title: str
    url: str
    text: str


@dataclass
class EvaluationResult:
    overall_score: float
    relevance: float
    grounding: float
    completeness: float
    clarity: float
    citation_coverage: float
    strengths: list[str] = field(default_factory=list)
    weaknesses: list[str] = field(default_factory=list)
    verdict: str = ""


@dataclass
class ResearchState:
    query: str
    planned_queries: list[str] = field(default_factory=list)
    search_results: list[dict[str, Any]] = field(default_factory=list)
    documents: list[SourceDocument] = field(default_factory=list)
    chunks: list[ChunkRecord] = field(default_factory=list)
    selected_chunks: list[ChunkRecord] = field(default_factory=list)
    report: str = ""
    refined_report: str = ""
    evaluation: EvaluationResult | None = None
    metrics: dict[str, Any] = field(default_factory=dict)
    logs: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
