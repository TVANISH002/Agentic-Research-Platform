# from __future__ import annotations

# import time
# from agents.planner import plan_queries
# from agents.writer import write_report, rewrite_report
# from agents.evaluator import evaluate_report
# from core.state import ResearchState
# from evaluation.summary import build_evidence_summary
# from rag.chunking import build_chunks
# from rag.retrieval import SemanticRetriever
# from tools.search_tools import run_web_search
# from tools.scrape_tools import scrape_many
# from core.config import settings


# def _start_timer(metrics: dict, name: str) -> float:
#     metrics.setdefault("latency_seconds", {})
#     return time.perf_counter()


# def _stop_timer(metrics: dict, name: str, start: float) -> None:
#     metrics["latency_seconds"][name] = round(time.perf_counter() - start, 3)


# def run_agentic_research(topic: str) -> ResearchState:
#     state = ResearchState(query=topic, metrics={})

#     total_start = time.perf_counter()

#     try:
#         start = _start_timer(state.metrics, "planning")
#         state.planned_queries = plan_queries(topic)
#         if not state.planned_queries:
#             state.planned_queries = [topic]
#         state.logs.append(f"Planner created {len(state.planned_queries)} subqueries.")
#         _stop_timer(state.metrics, "planning", start)

#         start = _start_timer(state.metrics, "search")
#         all_results: list[dict] = []
#         seen_urls: set[str] = set()
#         for query in state.planned_queries:
#             results = run_web_search(query)
#             for item in results:
#                 url = item.get("url")
#                 if url and url not in seen_urls:
#                     all_results.append(item)
#                     seen_urls.add(url)
#         state.search_results = all_results
#         state.metrics["search_result_count"] = len(all_results)
#         state.logs.append(f"Search returned {len(all_results)} unique results.")
#         _stop_timer(state.metrics, "search", start)

#         start = _start_timer(state.metrics, "scraping")
#         state.documents = scrape_many(all_results)
#         state.metrics["document_count"] = len(state.documents)
#         state.logs.append(f"Scraped {len(state.documents)} documents successfully.")
#         _stop_timer(state.metrics, "scraping", start)

#         start = _start_timer(state.metrics, "chunking_indexing")
#         state.chunks = build_chunks(state.documents)
#         retriever = SemanticRetriever()
#         retriever.index(state.chunks)
#         state.metrics["chunk_count"] = len(state.chunks)
#         state.logs.append(f"Built semantic index with {len(state.chunks)} chunks.")
#         _stop_timer(state.metrics, "chunking_indexing", start)

#         start = _start_timer(state.metrics, "retrieval")
#         state.selected_chunks = retriever.retrieve([topic] + state.planned_queries)
#         state.metrics["retrieved_chunk_count"] = len(state.selected_chunks)
#         _stop_timer(state.metrics, "retrieval", start)

#         start = _start_timer(state.metrics, "writing")
#         state.report = write_report(topic, state.selected_chunks, state.planned_queries)
#         _stop_timer(state.metrics, "writing", start)

#         start = _start_timer(state.metrics, "evaluation")
#         evidence_summary = build_evidence_summary(state.selected_chunks)
#         state.evaluation = evaluate_report(topic, state.report, evidence_summary)
#         _stop_timer(state.metrics, "evaluation", start)

#         if state.evaluation.overall_score < settings.evaluation_threshold:
#             start = _start_timer(state.metrics, "refinement")
#             state.refined_report = rewrite_report(
#                 topic=topic,
#                 report=state.report,
#                 weaknesses=state.evaluation.weaknesses,
#                 chunks=state.selected_chunks,
#             )
#             refined_eval = evaluate_report(topic, state.refined_report, evidence_summary)
#             if refined_eval.overall_score >= state.evaluation.overall_score:
#                 state.report = state.refined_report
#                 state.evaluation = refined_eval
#                 state.logs.append("Refinement loop improved the report.")
#             else:
#                 state.logs.append("Refinement loop ran, but original report scored better.")
#             _stop_timer(state.metrics, "refinement", start)
#         else:
#             state.logs.append("Report passed evaluation threshold on first attempt.")

#     except Exception as exc:
#         state.errors.append(str(exc))
#         state.logs.append("Pipeline encountered an error.")

#     state.metrics["total_latency_seconds"] = round(time.perf_counter() - total_start, 3)
#     return state


from __future__ import annotations

import time

from agents.planner import plan_queries
from agents.writer import write_report, rewrite_report
from agents.evaluator import evaluate_report
from core.state import ResearchState
from evaluation.summary import build_evidence_summary
from rag.chunking import build_chunks
from rag.retrieval import SemanticRetriever
from tools.search_tools import run_web_search
from tools.scrape_tools import scrape_many
from core.config import settings


def _start_timer(metrics: dict, name: str) -> float:
    metrics.setdefault("latency_seconds", {})
    return time.perf_counter()


def _stop_timer(metrics: dict, name: str, start: float) -> None:
    metrics["latency_seconds"][name] = round(time.perf_counter() - start, 3)


def run_agentic_research(topic: str) -> ResearchState:
    state = ResearchState(query=topic, metrics={})
    total_start = time.perf_counter()

    try:
        # -------------------------
        # 1. Planning
        # -------------------------
        start = _start_timer(state.metrics, "planning")
        state.planned_queries = plan_queries(topic)

        if not state.planned_queries:
            state.planned_queries = [{"query": topic, "type": "fallback"}]

        state.logs.append(f"Planner created {len(state.planned_queries)} subqueries.")
        _stop_timer(state.metrics, "planning", start)

        # Extract only plain query strings when needed later
        query_texts = [
            q["query"]
            for q in state.planned_queries
            if isinstance(q, dict) and "query" in q
        ]

        # -------------------------
        # 2. Search
        # -------------------------
        start = _start_timer(state.metrics, "search")
        all_results = run_web_search(state.planned_queries)
        state.search_results = all_results
        state.metrics["search_result_count"] = len(all_results)
        state.logs.append(f"Search returned {len(all_results)} unique results.")
        _stop_timer(state.metrics, "search", start)

        # -------------------------
        # 3. Scraping
        # -------------------------
        start = _start_timer(state.metrics, "scraping")
        state.documents = scrape_many(all_results)
        state.metrics["document_count"] = len(state.documents)
        state.logs.append(f"Scraped {len(state.documents)} documents successfully.")
        _stop_timer(state.metrics, "scraping", start)

        # -------------------------
        # 4. Chunking + Indexing
        # -------------------------
        start = _start_timer(state.metrics, "chunking_indexing")
        state.chunks = build_chunks(state.documents)
        retriever = SemanticRetriever()
        retriever.index(state.chunks)
        state.metrics["chunk_count"] = len(state.chunks)
        state.logs.append(f"Built semantic index with {len(state.chunks)} chunks.")
        _stop_timer(state.metrics, "chunking_indexing", start)

        # -------------------------
        # 5. Retrieval
        # -------------------------
        start = _start_timer(state.metrics, "retrieval")
        state.selected_chunks = retriever.retrieve([topic] + query_texts)
        state.metrics["retrieved_chunk_count"] = len(state.selected_chunks)
        _stop_timer(state.metrics, "retrieval", start)

        # -------------------------
        # 6. Writing
        # -------------------------
        start = _start_timer(state.metrics, "writing")
        state.report = write_report(topic, state.selected_chunks, query_texts)
        _stop_timer(state.metrics, "writing", start)

        # -------------------------
        # 7. Evaluation
        # -------------------------
        start = _start_timer(state.metrics, "evaluation")
        evidence_summary = build_evidence_summary(state.selected_chunks)
        state.evaluation = evaluate_report(topic, state.report, evidence_summary)
        _stop_timer(state.metrics, "evaluation", start)

        # -------------------------
        # 8. Refinement
        # -------------------------
        if state.evaluation.overall_score < settings.evaluation_threshold:
            start = _start_timer(state.metrics, "refinement")
            state.refined_report = rewrite_report(
                topic=topic,
                report=state.report,
                weaknesses=state.evaluation.weaknesses,
                chunks=state.selected_chunks,
            )
            refined_eval = evaluate_report(topic, state.refined_report, evidence_summary)

            if refined_eval.overall_score >= state.evaluation.overall_score:
                state.report = state.refined_report
                state.evaluation = refined_eval
                state.logs.append("Refinement loop improved the report.")
            else:
                state.logs.append("Refinement loop ran, but original report scored better.")

            _stop_timer(state.metrics, "refinement", start)
        else:
            state.logs.append("Report passed evaluation threshold on first attempt.")

    # except Exception as exc:
    #     state.errors.append(str(exc))
    #     state.logs.append("Pipeline encountered an error.")
        
    except Exception as exc:
        import traceback
        state.errors.append(f"{type(exc).__name__}: {str(exc)}")
        state.logs.append(f"Pipeline encountered an error at runtime: {type(exc).__name__}")
        state.logs.append(traceback.format_exc())    

    state.metrics["total_latency_seconds"] = round(time.perf_counter() - total_start, 3)
    return state