# Enterprise Multi-Source RAG + Agentic Analytics Platform

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
pip install -r requirements.txt
cp .env.example .env
python -m src.data.generate_synthetic_data
python -m src.data.load_duckdb
python -m src.knowledge.generate_sources
uvicorn src.api.main:app --reload
```

Start Streamlit:
```bash
streamlit run streamlit_app.py
```

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
```bash
pytest -q
python -m src.evaluation.run_eval
```

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
