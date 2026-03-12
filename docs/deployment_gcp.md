# Deployment on GCP

1. Create BigQuery dataset and run `src/data/bigquery_ddl.sql`.
2. Load warehouse + knowledge docs from Cloud Storage.
3. Configure profile `enterprise_vertex` or `enterprise_openai` in Cloud Run environment variables.
4. Use Vertex Gemini/OpenAI for LLM, Vertex/OpenAI for embeddings, and Qdrant/pgvector/Vector Search for retrieval.
5. Export observability events to Cloud Logging and BigQuery sink.
