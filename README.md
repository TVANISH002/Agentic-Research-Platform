````md
# Agentic Research Intelligence Platform

A multi-agent research assistant that evolved from a Phase 2 agentic RAG prototype into a more stable, better-structured, and recruiter-ready research workflow system.

The project is designed to answer research-style questions through a multi-stage pipeline that combines planning, live web search, scraping, semantic retrieval, grounded report generation, and evaluation-driven refinement.

## What the system does

The workflow currently includes:

- planner-driven subquery generation
- multi-source web retrieval
- live source deduplication and ranking
- document scraping and chunking
- semantic evidence retrieval with embeddings
- citation-aware report generation
- structured evaluation and refinement loop
- Streamlit observability dashboard

## Phase 2 — Core Agentic RAG Workflow

Phase 2 focused on building the first end-to-end multi-agent research workflow.

### Added in Phase 2
- Built a **6-stage agentic workflow** across:
  - planning
  - search
  - scraping
  - retrieval
  - synthesis
  - evaluation
- Added **planner-driven subquery generation**
- Added **multi-source Tavily web search**
- Added **document scraping** for live pages
- Added **chunking + semantic retrieval** using sentence-transformer embeddings
- Added **citation-aware report generation**
- Added an **evaluation and refinement loop**
- Added **latency tracking** across major workflow stages
- Built a **50+ query evaluation workflow** to test relevance, grounding, and completeness across different research-style prompts
- Built the first **Streamlit dashboard** for observability

### Goal of Phase 2
The goal of Phase 2 was to move beyond a simple prompt-based demo and build a full research-oriented workflow that could retrieve evidence, generate grounded answers, and evaluate output quality.

## Phase 3 — Pipeline Stabilization, Structured Search, and UI Polish

Phase 3 focused on making the system more stable, better integrated, and easier to demo.

### Added / improved in Phase 3
- Upgraded the **planner** to generate more structured subqueries with query types such as:
  - overview
  - technical
  - recent
  - risks
- Refactored the **search layer** to support planner-generated multi-query retrieval
- Added:
  - duplicate URL removal
  - lightweight result scoring
  - total search-result limiting
- Refactored the **orchestrator** so planner, search, retrieval, writing, and evaluation stages pass data in the correct format
- Fixed document flow mismatches between:
  - scraper output
  - chunking
  - UI display
- Updated **chunking** to work cleanly with dict-based scraped documents
- Added missing config support such as:
  - `max_total_results`
- Improved **LLM reliability and debugging visibility**
- Improved **latency awareness** and pipeline-stage logs
- Redesigned the **Streamlit UI** to make the project more polished and recruiter/demo friendly

### Goal of Phase 3
The goal of Phase 3 was to turn the project from a working prototype into a more stable, cleaner, and better-presented end-to-end system.

## Phase 4 — Planned Improvements

Phase 4 will focus on retrieval quality, source quality control, and performance improvements.

### Planned for Phase 4
- Parallelize more of the end-to-end workflow to reduce latency
- Improve the retrieval stage with stronger evidence-selection logic
- Add **domain trust scoring** for better source prioritization
- Add **source credibility scoring** to reduce weak or noisy sources
- Explore **second-stage reranking inside retrieval**
- Add **manual whitelist / blacklist controls** for domain filtering
- Improve source filtering so the system is less affected by duplicate or low-quality pages
- Reduce prompt noise before writing and evaluation
- Improve observability and latency control further
- Continue balancing answer quality, grounding, and system efficiency

### Goal of Phase 4
The goal of Phase 4 is to make the system faster, more reliable, and stronger in evidence selection without changing the core 6-stage project story.

## Architecture

- **Planner Agent** decomposes the user topic into focused research subqueries.
- **Search Layer** pulls multiple live results from Tavily for those subqueries.
- **Reader Layer** scrapes selected pages and preserves source metadata.
- **RAG Layer** chunks documents and indexes them with sentence-transformer embeddings.
- **Retriever** selects the most relevant evidence for the original topic and planner-generated subqueries.
- **Writer Agent** creates a citation-aware report using retrieved evidence.
- **Evaluator Agent** scores the report on relevance, grounding, completeness, clarity, and citation coverage.
- **Refinement Loop** rewrites the report when the score falls below threshold.
- **Streamlit UI** shows subqueries, sources, evidence, final report, logs, and latency metrics.

## End-to-End Workflow

1. The user gives one research question.
2. The planner breaks that question into multiple focused subqueries.
3. Tavily searches each subquery and returns live web results.
4. The system combines those results, removes duplicate URLs, and ranks them.
5. The top-ranked URLs are scraped and converted into structured source documents.
6. The scraped documents are chunked into smaller text segments.
7. The retriever compares chunk embeddings against both the original query and planner-generated subqueries.
8. The top retrieved chunks are selected as final evidence.
9. The writer uses those chunks to generate a grounded report.
10. The evaluator checks whether the report is relevant, grounded, and complete.
11. If the score is too low, the refinement loop rewrites the report and re-evaluates it.

## Evaluation Strategy

To move beyond demo-based testing, the project includes a **50+ query evaluation workflow** covering:
- overview questions
- technical architecture questions
- recent developments
- risks and limitations
- comparison prompts
- practical use-case questions

The evaluation process was used to assess:
- **relevance** — whether the answer addressed the query
- **grounding / faithfulness** — whether the answer stayed supported by retrieved evidence
- **completeness** — whether the answer covered enough of the topic to be useful

This evaluation workflow helped surface weakly grounded outputs and guided improvements in retrieval quality and overall system behavior.

## Project Structure

```text
agentic_research_platform/
├── agents/
│   ├── planner.py
│   ├── writer.py
│   └── evaluator.py
├── core/
│   ├── config.py
│   ├── llm.py
│   ├── orchestrator.py
│   └── state.py
├── evaluation/
│   └── summary.py
├── rag/
│   ├── chunking.py
│   └── retrieval.py
├── tools/
│   ├── scrape_tools.py
│   └── search_tools.py
├── app.py
├── README.md
└── requirements.txt
````

## Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
GROQ_MODEL=llama-3.3-70b-versatile
```

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Good Groq Model Defaults

* `llama-3.3-70b-versatile` → strong quality-oriented default
* `meta-llama/llama-4-scout-17b-16e-instruct` → better TPM budget for heavier research workflows
* `llama-3.1-8b-instant` → faster / cheaper fallback
* `openai/gpt-oss-20b` → alternative experimental option if enabled

## Deployment

Use a Python service or Streamlit-compatible web service.

```bash
streamlit run app.py --server.port $PORT --server.address 0.0.0.0
```

```
```
