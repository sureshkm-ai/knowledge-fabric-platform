# Building an Enterprise Multi-Source RAG + Agentic Analytics Assistant

Enterprise AI assistants fail when they mix brittle SQL generation, weak retrieval, and ungoverned evidence. This project demonstrates an opinionated architecture: semantic-layer-first SQL, hybrid retrieval for unstructured knowledge, and LangGraph orchestration with explicit validation.

## Why semantic layers matter
Raw fact tables are unsafe for agentic SQL. We expose only curated semantic views with trusted KPI definitions.

## Hybrid retrieval
Vector search handles semantic matching while BM25 recovers exact-policy language and SKU/entity terms.

## LangGraph workflow
The graph routes questions to structured, doc, or mixed paths and enforces evidence validation before answer synthesis.

## Governance and access control
RBAC + ABAC filters are applied to SQL and document retrieval before prompt construction.

## Evaluation
We track route accuracy, retrieval metrics (Recall@K/Precision@K/MRR/nDCG), and grounding keyword scores.

## Migration to cloud
Swap profile from `local` to `enterprise_openai` or `enterprise_vertex`; orchestration remains unchanged while providers change through factories.
