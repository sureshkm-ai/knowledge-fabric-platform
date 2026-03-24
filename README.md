# Enterprise Multi-Source RAG + Agentic Analytics Platform

<<<<<<< HEAD
[![CI](https://img.shields.io/badge/ci-github%20actions-blue)](.github/workflows/ci.yml)
[![Python 3.11](https://img.shields.io/badge/python-3.11-3776AB)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/api-fastapi-009688)](https://fastapi.tiangolo.com/)
[![LangGraph](https://img.shields.io/badge/orchestration-langgraph-black)](https://github.com/langchain-ai/langgraph)

A portfolio-grade reference implementation for **enterprise retail/CPG analytics copilots** that combines:
- governed structured analytics from a semantic SQL layer,
- unstructured policy/SOP/analyst knowledge,
- hybrid retrieval,
- and explicit evidence validation before LLM synthesis.

---

## Why this project exists

Enterprise GenAI systems fail when they:
1. query raw warehouse facts unsafely,
2. retrieve irrelevant policy docs,
3. synthesize answers without evidence checks,
4. and lack governance + observability.

This repository demonstrates a production-style architecture that addresses those failure modes while staying locally runnable.

---

## Core capabilities

- **Semantic-layer-first SQL**: only approved semantic views are queryable.
- **Hybrid retrieval**: vector similarity + BM25 lexical search + reranking.
- **Real provider integrations**:
  - LLM: OpenAI, Azure OpenAI, Vertex Gemini.
  - Embeddings: OpenAI, Vertex text embeddings, sentence-transformers for local.
  - Vector stores: FAISS (local), Qdrant, pgvector.
- **LangGraph-style orchestration**: route planning (`structured` / `doc` / `mixed`) and explicit workflow stages.
- **Governance**: role + region scoped SQL and document access.
- **Observability**: trace events, route decisions, validation outcomes, diagnostics.
- **Evaluation**: route accuracy, grounding score, and retrieval ranking metrics.

---

## Architecture overview

```text
Client (Streamlit/UI/HTTP)
  -> FastAPI /ask
     -> Orchestration graph
        -> plan
        -> extract_entities
        -> prepare_sql (semantic views only)
        -> run_sql (guardrails + scope)
        -> retrieve_docs (hybrid retriever + metadata filter)
        -> validate_evidence
        -> synthesize_answer
     -> structured trace logging
```

See `docs/architecture_diagram.md` for the deployment-oriented view.

---

## Environment profiles

| Profile | LLM provider | Embedding provider | Vector store | SQL backend | Observability |
|---|---|---|---|---|---|
| `local` | OpenAI-compatible (mock fallback) | sentence-transformers | FAISS | DuckDB | JSONL |
| `enterprise_openai` | OpenAI/Azure OpenAI | OpenAI embeddings | Qdrant or pgvector | BigQuery | BigQuery/structured logs |
| `enterprise_vertex` | Vertex Gemini | Vertex text embeddings | Vertex VS / pgvector / Qdrant | BigQuery | Cloud Logging + BQ sink |

The orchestration/business logic remains profile-agnostic; only provider factories change.

---

## Repository layout

```text
src/
  api/            FastAPI service
  agents/         SQL guardrails + runner
  config/         profiles/settings/provider registry
  data/           synthetic warehouse data + semantic SQL
  embeddings/     embedding providers + factory
  evaluation/     datasets, metrics, judge, runner
  knowledge/      synthetic docs + chunk/entity pipelines
  langgraph_app/  workflow state, nodes, graph, runner
  llm/            LLM providers + factory
  observability/  trace schema/logger/reports
  retrieval/      BM25/vector/hybrid/reranker
  security/       RBAC/ABAC policy & filters
  vectorstore/    FAISS/Qdrant/pgvector adapters
```

---

## Local quickstart

```bash
python -m venv .venv
source .venv/bin/activate
=======
Portfolio-grade reference architecture for an enterprise retail/CPG analytics assistant that combines governed warehouse analytics and unstructured enterprise knowledge with LangGraph orchestration.

## Highlights
- **Semantic-layer-first SQL**: agent queries only approved semantic views.
- **Hybrid retrieval**: vector + BM25 + reranking + metadata filters.
- **Real provider support**: OpenAI, Azure OpenAI, Vertex Gemini; OpenAI/Vertex embeddings; FAISS/Qdrant/pgvector vector stores.
- **Governance**: RBAC/ABAC for SQL and documents.
- **Observability & eval**: trace logging, route metrics, retrieval metrics.

## Architecture overview
1. FastAPI receives question and access context.
2. LangGraph-style workflow plans route (`structured`, `doc`, `mixed`).
3. SQL path uses guardrailed semantic views.
4. Retrieval path uses hybrid retriever over enterprise docs.
5. Evidence validation checks scope, sufficiency, and consistency.
6. LLM synthesizes grounded response.

## Profiles
| Profile | LLM | Embeddings | Vector DB | SQL | Observability |
|---|---|---|---|---|---|
| `local` | OpenAI-compatible (+mock fallback) | sentence-transformers | FAISS | DuckDB | JSONL |
| `enterprise_openai` | OpenAI/Azure OpenAI | OpenAI embeddings | Qdrant/pgvector | BigQuery | BigQuery/structured logs |
| `enterprise_vertex` | Vertex Gemini | Vertex embeddings | pgvector/Qdrant/Vector Search | BigQuery | Cloud Logging + BQ sink |

## Quickstart (local)
```bash
python -m venv .venv && source .venv/bin/activate
>>>>>>> main
pip install -r requirements.txt
cp .env.example .env
python -m src.data.generate_synthetic_data
python -m src.data.load_duckdb
python -m src.knowledge.generate_sources
uvicorn src.api.main:app --reload
```

<<<<<<< HEAD
Open Streamlit demo:
=======
Start Streamlit:
>>>>>>> main
```bash
streamlit run streamlit_app.py
```

<<<<<<< HEAD
---

## Enterprise setup

Set profile and credentials in `.env`:

### `enterprise_openai`
- `APP_PROFILE=enterprise_openai`
- `OPENAI_API_KEY` or `AZURE_OPENAI_API_KEY`
- `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_API_VERSION`
- `QDRANT_URL` / `QDRANT_API_KEY` or `PGVECTOR_DSN`

### `enterprise_vertex`
- `APP_PROFILE=enterprise_vertex`
- `VERTEX_PROJECT_ID`, `VERTEX_LOCATION`
- `QDRANT_URL` or `PGVECTOR_DSN`
- BigQuery dataset/service account for SQL execution path

---

## API endpoints

- `GET /health`
- `POST /ask`
- `POST /ask/v2`
- `GET /trace/{trace_id}`

Example request:

```json
{
  "question": "Why did Texas snack sales decline and what actions should we take?",
  "role": "manager",
  "allowed_regions": ["US-SOUTH"],
  "business_units": ["snacks"],
  "include_evidence": true
}
```

---

## Evaluation

=======
## Enterprise setup
Set `APP_PROFILE=enterprise_openai` or `enterprise_vertex`, then configure provider credentials in `.env`:
- OpenAI/Azure: `OPENAI_API_KEY` or `AZURE_OPENAI_*`
- Vertex: `VERTEX_PROJECT_ID`, `VERTEX_LOCATION`
- Vector stores: `QDRANT_URL`, `QDRANT_API_KEY` or `PGVECTOR_DSN`

## API endpoints
- `GET /health`
- `POST /ask`
- `POST /ask/v2`
- `GET /trace/{id}`

## Example questions
- "What is the Texas snack sales trend and what policy actions are recommended?"
- "What does the allocation override SOP require for high-risk inventory?"
- "Did promo P001 improve net sales in US-SOUTH?"

## Evaluation
>>>>>>> main
```bash
pytest -q
python -m src.evaluation.run_eval
```

<<<<<<< HEAD
---

## Deployment

- Cloud deployment guidance: `docs/deployment_gcp.md`
- Architecture narrative: `docs/architecture_diagram.md`
- Semantic safety rationale: `docs/semantic_layer.md`

---

## Blog and portfolio artifacts

- `docs/blog_outline.md`
- `docs/blog_draft.md`

---

## Interview talking points

- Why semantic layers are mandatory for agentic SQL.
- How hybrid retrieval improves policy + KPI grounding.
- How profile-driven architecture enables local-to-enterprise migration.
- Why evidence validation and observability are non-negotiable for enterprise trust.
=======
## Deployment notes
See `docs/deployment_gcp.md` and `docs/architecture_diagram.md`.

## Demo screenshots
- TODO placeholder 1
- TODO placeholder 2

## Interview talking points
- Semantic-layer safety and enterprise SQL governance
- Profile-driven architecture and provider abstraction
- Hybrid retrieval + evidence validation for grounded analytics
- Observability and offline evaluation for production readiness
>>>>>>> main
