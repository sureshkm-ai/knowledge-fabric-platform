<<<<<<< HEAD
# Architecture Diagram (Narrative)

## Request lifecycle

```text
User/BI Analyst
  -> FastAPI (/ask)
    -> Access context (role, region, BU)
    -> Orchestration graph (LangGraph-style)
       1) plan route
       2) extract entities
       3) prepare SQL (semantic layer only)
       4) run SQL (guardrails + scope filters)
       5) retrieve docs (vector + BM25 + rerank + metadata filter)
       6) validate evidence
       7) synthesize answer (LLM)
    -> Return answer + evidence + diagnostics
    -> Emit trace events
```

## Local profile architecture
- DuckDB warehouse simulation
- FAISS-like local vector index
- sentence-transformers embeddings
- JSONL observability sink

## Enterprise profile architecture
- BigQuery semantic layer execution service
- Managed embeddings (OpenAI/Vertex)
- Managed vector store (Qdrant/pgvector/Vertex Vector Search)
- Cloud Run hosting for API
- Cloud Logging + BigQuery observability sink

## Governance boundaries
- SQL can only reference approved semantic views.
- Region/business-unit scope is enforced before SQL execution.
- Documents are filtered by metadata and role classification.
- Evidence validation runs before final synthesis.
=======
# Architecture (Text Diagram)

User -> FastAPI `/ask` -> LangGraph workflow
- plan/extract entities
- semantic SQL prep + guardrails
- SQL execution (DuckDB/BigQuery)
- hybrid retrieval (vector + BM25 + rerank)
- evidence validation
- LLM synthesis

Cross-cutting: RBAC/ABAC, observability, evaluation.
>>>>>>> main
