# Agentic Research Intelligence Platform

A multi-agent research workflow for grounded question answering over live web sources.

This project goes beyond a simple LLM prompt-and-response demo by combining structured query planning, multi-source retrieval, document scraping, semantic evidence selection, citation-aware report generation, and evaluation-driven refinement in a single end-to-end pipeline.

The goal is to answer research-style questions in a way that is more **grounded**, **traceable**, and **systematic** than a standard chatbot workflow.

---

## Highlights

* Multi-agent research pipeline across planning, search, scraping, retrieval, writing, and evaluation
* Planner-driven subquery generation for better topic coverage
* Multi-source live web retrieval using Tavily
* Document scraping with source metadata preservation
* Semantic chunk retrieval using sentence-transformer embeddings
* Citation-aware report generation
* Structured evaluation on relevance, grounding, and completeness
* Refinement loop for weak initial outputs
* Streamlit dashboard for observability, evidence inspection, and latency tracking

---

## Why this project matters

Research-style AI questions are harder than normal chat questions.

A standard LLM can produce fluent answers, but those answers may:

* rely too much on model memory
* miss important parts of the topic
* be weakly grounded in real sources
* be difficult to trace back to supporting evidence

This project addresses that by turning one user question into a full research workflow:

* plan the topic
* gather live sources
* extract evidence
* retrieve the strongest chunks
* generate a grounded report
* evaluate the output quality

---

## System Architecture

The current workflow includes six main stages:

1. **Planner Agent**
   Breaks the user topic into focused research subqueries.

2. **Search Layer**
   Sends those subqueries to Tavily and collects live web results.

3. **Reader Layer**
   Scrapes selected pages and preserves source metadata.

4. **RAG Layer / Retriever**
   Chunks documents, builds embeddings, and selects the most relevant evidence for the original query and planner-generated subqueries.

5. **Writer Agent**
   Generates a citation-aware report from retrieved evidence.

6. **Evaluator Agent**
   Scores the report on relevance, grounding, completeness, clarity, and citation coverage, and triggers refinement if needed.

---

## End-to-End Workflow

1. The user asks one research question.
2. The planner expands that question into multiple focused subqueries.
3. Tavily searches each subquery and returns live results.
4. The system combines results, removes duplicate URLs, and ranks them.
5. The highest-ranked URLs are scraped into source documents.
6. The source text is chunked into smaller evidence segments.
7. The retriever compares chunk embeddings against the original query and planner-generated subqueries.
8. The top evidence chunks are selected.
9. The writer generates a grounded report from those chunks.
10. The evaluator checks whether the answer is relevant, grounded, and complete.
11. If needed, the refinement loop rewrites and re-evaluates the report.

---

## Example Retrieval Flow

For a user query like:

**“Explain vectorless RAG”**

the planner may generate subqueries such as:

* what is vectorless RAG
* vectorless RAG architecture
* latest vectorless RAG updates
* vectorless RAG limitations and challenges

Those subqueries are searched independently, their results are merged and deduplicated, and only the strongest sources are scraped.

The retrieved documents are then chunked, and the retriever ranks chunks against:

* the original user query
* the overview subquery
* the technical subquery
* the recent-updates subquery
* the risks/limitations subquery

This allows the final answer to cover multiple angles of the topic instead of relying on only one search phrasing.

---

## Evaluation Strategy

To move beyond single-demo testing, the project includes a **50+ query evaluation workflow** covering:

* overview questions
* technical architecture questions
* recent developments
* risks and limitations
* comparison prompts
* practical use-case questions

The evaluation process focuses on:

* **Relevance** — did the answer actually address the question?
* **Grounding / Faithfulness** — was the answer supported by retrieved evidence?
* **Completeness** — did the answer cover enough of the topic to be useful?

This helped identify weakly grounded outputs and guided improvements to retrieval quality and overall system behavior.

---

## Project Roadmap

### Phase 2 — Core Agentic RAG Workflow

Phase 2 established the first end-to-end research pipeline.

**Added in Phase 2**

* 6-stage agentic workflow across planning, search, scraping, retrieval, synthesis, and evaluation
* planner-driven subquery generation
* multi-source Tavily search
* live page scraping
* chunking and semantic retrieval with embeddings
* citation-aware report generation
* evaluation and refinement loop
* latency tracking across workflow stages
* initial Streamlit dashboard
* 50+ query evaluation workflow

### Phase 3 — Pipeline Stabilization and UI Polish

Phase 3 focused on reliability, integration quality, and presentation.

**Added / improved in Phase 3**

* more structured planner-generated subqueries
* multi-query search orchestration
* duplicate URL removal and lightweight result scoring
* cleaner orchestration between planner, search, retrieval, writing, and evaluation
* chunking updates for dict-based scraped documents
* improved config support such as `max_total_results`
* better LLM reliability and debugging visibility
* improved stage-level logs and latency awareness
* cleaner, more polished Streamlit interface for demos and recruiter review

### Phase 4 — Planned Improvements

Phase 4 is focused on retrieval quality, source quality control, and performance improvements.

**Planned for Phase 4**

* parallelize more of the workflow to reduce latency
* strengthen evidence selection inside retrieval
* add domain trust scoring
* add source credibility scoring
* explore reranking inside the retrieval stage
* add manual whitelist / blacklist controls for domains
* improve source filtering for noisy or duplicate pages
* reduce prompt noise before writing and evaluation
* continue improving the balance between answer quality and system efficiency

---

## Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
GROQ_MODEL=llama-3.3-70b-versatile
```

---

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## Recommended Groq Models

* `llama-3.3-70b-versatile` → strong quality-oriented default
* `meta-llama/llama-4-scout-17b-16e-instruct` → better TPM budget for heavier research workflows
* `llama-3.1-8b-instant` → faster / cheaper fallback
* `openai/gpt-oss-20b` → experimental alternative if enabled on your account

---

## Deployment

For local development:

```bash
streamlit run app.py
```

For deployment environments that provide a runtime port:

```bash
streamlit run app.py --server.port $PORT --server.address 0.0.0.0
```
