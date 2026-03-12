# Architecture (Text Diagram)

User -> FastAPI `/ask` -> LangGraph workflow
- plan/extract entities
- semantic SQL prep + guardrails
- SQL execution (DuckDB/BigQuery)
- hybrid retrieval (vector + BM25 + rerank)
- evidence validation
- LLM synthesis

Cross-cutting: RBAC/ABAC, observability, evaluation.
