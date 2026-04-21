# Agentic Research Intelligence Platform

A Phase-2 upgrade of a multi-agent research assistant into a more advanced **agentic RAG system** with:
- planner-driven subquery generation
- multi-source web retrieval
- document scraping and chunking
- semantic evidence retrieval with embeddings
- citation-aware report generation
- structured evaluation and refinement loop
- Streamlit observability dashboard

## Architecture
1. **Planner Agent** decomposes the topic into focused web research queries.
2. **Search Layer** pulls multiple live results from Tavily.
3. **Reader Layer** scrapes several pages and preserves source metadata.
4. **RAG Layer** chunks documents and indexes them with sentence-transformer embeddings.
5. **Retriever** selects the most relevant evidence for the topic and subqueries.
6. **Writer Agent** creates a citation-aware report using `[S1]` style source tags.
7. **Evaluator Agent** scores the report on relevance, grounding, completeness, clarity, and citation coverage.
8. **Refinement Loop** rewrites the report when the score is below threshold.
9. **Streamlit UI** shows subqueries, sources, evidence, final report, logs, and latency metrics.

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
```

## Environment Variables
Create a `.env` file:

```bash
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
- `llama-3.3-70b-versatile` → best default balance for quality
- `llama-3.1-8b-instant` → fastest/cheapest fallback
- `openai/gpt-oss-20b` → strong alternative for experimentation if enabled on your account

## Render Deployment
Use a Python service or Streamlit-compatible web service.
Start command:
```bash
streamlit run app.py --server.port $PORT --server.address 0.0.0.0
```
