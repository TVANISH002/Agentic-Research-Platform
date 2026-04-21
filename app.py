from __future__ import annotations

import pandas as pd
import streamlit as st
from core.config import settings
from core.orchestrator import run_agentic_research

st.set_page_config(page_title="Agentic Research Intelligence Platform", layout="wide")

st.title("🧠 Agentic Research Intelligence Platform")
st.caption("Phase 2: multi-source retrieval, semantic evidence selection, citation-aware writing, and evaluation-driven refinement.")

with st.sidebar:
    st.header("Settings")
    st.write(f"**Model:** {settings.groq_model}")
    st.write(f"**Embedding model:** {settings.embedding_model}")
    st.info("Required env vars: GROQ_API_KEY, TAVILY_API_KEY")

query = st.text_input("Enter a research topic", placeholder="Example: Latest progress in multimodal RAG for enterprise search")
run = st.button("Run Research Pipeline", type="primary")

if run and query:
    with st.spinner("Running planner, retrieval, writing, evaluation, and refinement..."):
        state = run_agentic_research(query)

    if state.errors:
        st.error("Pipeline encountered errors:")
        for err in state.errors:
            st.code(err)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Sources scraped", state.metrics.get("document_count", 0))
    c2.metric("Chunks indexed", state.metrics.get("chunk_count", 0))
    c3.metric("Chunks retrieved", state.metrics.get("retrieved_chunk_count", 0))
    c4.metric("Total latency (s)", state.metrics.get("total_latency_seconds", 0))

    st.subheader("📌 Planned subqueries")
    for item in state.planned_queries:
        st.write(f"- {item}")

    st.subheader("📰 Source documents")
    for doc in state.documents:
        with st.expander(f"{doc.source_id} — {doc.title}"):
            st.write(doc.url)
            st.write(doc.snippet)
            st.write(doc.content[:1500] + ("..." if len(doc.content) > 1500 else ""))

    st.subheader("🔎 Retrieved evidence chunks")
    for chunk in state.selected_chunks:
        with st.expander(f"{chunk.chunk_id} | {chunk.title}"):
            st.write(chunk.url)
            st.write(chunk.text)

    st.subheader("📝 Final report")
    st.markdown(state.report)

    if state.evaluation:
        st.subheader("📊 Evaluation")
        eval_df = pd.DataFrame(
            [{
                "overall_score": state.evaluation.overall_score,
                "relevance": state.evaluation.relevance,
                "grounding": state.evaluation.grounding,
                "completeness": state.evaluation.completeness,
                "clarity": state.evaluation.clarity,
                "citation_coverage": state.evaluation.citation_coverage,
            }]
        )
        st.dataframe(eval_df, use_container_width=True)
        st.write("**Strengths**")
        for s in state.evaluation.strengths:
            st.write(f"- {s}")
        st.write("**Weaknesses**")
        for w in state.evaluation.weaknesses:
            st.write(f"- {w}")
        st.write(f"**Verdict:** {state.evaluation.verdict}")

    st.subheader("⏱️ Metrics")
    latency_df = pd.DataFrame([
        {"stage": k, "seconds": v}
        for k, v in state.metrics.get("latency_seconds", {}).items()
    ])
    st.dataframe(latency_df, use_container_width=True)

    st.subheader("🪵 Logs")
    for log in state.logs:
        st.write(f"- {log}")

elif run:
    st.warning("Please enter a topic.")
