# Deployment on GCP (Enterprise Profile)

## 1) Data platform
1. Create BigQuery dataset(s) for raw and semantic objects.
2. Apply DDL from `src/data/bigquery_ddl.sql` (adapt concrete schemas).
3. Materialize semantic views from `src/data/semantic_views.sql` in BigQuery SQL dialect.

## 2) Knowledge ingestion
1. Store policy/SOP/analyst docs in Cloud Storage.
2. Run chunking + metadata enrichment pipeline.
3. Embed docs with Vertex or OpenAI embeddings and upsert into vector store.

## 3) Serving layer
1. Build container from `Dockerfile`.
2. Deploy FastAPI to Cloud Run.
3. Set `APP_PROFILE=enterprise_vertex` or `APP_PROFILE=enterprise_openai`.

## 4) Provider configuration
- Vertex path: Gemini + Vertex text embeddings.
- OpenAI path: OpenAI/Azure OpenAI + OpenAI embeddings.
- Vector store: Qdrant / pgvector / Vertex Vector Search.

## 5) Governance and observability
- Enforce semantic-layer-only SQL access.
- Apply role/region/business-unit constraints in request context.
- Ship trace events to Cloud Logging and/or BigQuery sink.

## 6) Production hardening checklist
- Secret Manager for API credentials
- VPC egress controls
- SLOs + alerting for latency/error rate
- automated eval runs in CI/CD gate
