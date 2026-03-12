# Building a Production-Credible Enterprise RAG + Agentic Analytics Assistant

Enterprise leaders often ask: *"Can we trust an AI assistant with our metrics and policy decisions?"*  
The honest answer is: only if architecture enforces governance, evidence quality, and observability.

This project is a reference implementation for that bar.

## The real enterprise problem

Most "RAG demos" break in production because they:
- let LLMs query raw fact tables,
- ignore role/region access constraints,
- retrieve semantically similar but policy-invalid docs,
- and produce polished but weakly grounded answers.

In retail/CPG analytics, these failures lead to bad decisions about pricing, promotions, and inventory.

## Design principles used in this repository

1. **Semantic layer as contract**  
   The assistant never hits raw fact tables directly. It queries governed semantic views with trusted KPI definitions.

2. **Hybrid retrieval, not vector-only retrieval**  
   Policy language often contains exact terms (approval thresholds, SOP names). BM25 recovers those terms; vector retrieval recovers semantic paraphrases.

3. **Explicit orchestration**  
   A LangGraph-style flow makes each decision legible:
   `plan -> extract_entities -> prepare_sql -> run_sql -> retrieve_docs -> validate_evidence -> synthesize_answer`.

4. **Evidence validation before synthesis**  
   We validate evidence sufficiency, region/entity consistency, and relevance before answer generation.

5. **Profile-driven provider architecture**  
   The same business logic runs in:
   - `local` (DuckDB + FAISS + local embeddings),
   - `enterprise_openai`,
   - `enterprise_vertex`.

6. **Observability first**  
   Every request has trace events for route choice, SQL execution, retrieval outcomes, validation notes, and diagnostics.

## Why semantic layers matter more than prompt engineering

Prompt engineering can improve phrasing; it does not enforce governance.  
Semantic layers do:
- constrained joins,
- business-defined metrics,
- and bounded SQL surface area.

This is why the guardrails deny raw table access and non-SELECT statements.

## Retrieval architecture details

The retrieval stack uses:
- embedding-based similarity (FAISS/Qdrant/pgvector),
- BM25 lexical retrieval,
- score fusion,
- light reranking,
- metadata filters for access/governance.

This combination increases recall for both KPI/entity questions and exact policy language.

## Governance and access control

Governance is enforced in two places:
- **structured path**: SQL scoping by role, region, and business unit,
- **document path**: metadata-based access filtering before prompt construction.

This ensures a user with US-SOUTH access cannot receive US-WEST-only evidence.

## Evaluation strategy

The project includes:
- route accuracy,
- grounding keyword score,
- retrieval ranking metrics (Precision@K, Recall@K, MRR, nDCG).

This combination evaluates both orchestration quality and grounding quality.

## Local-to-enterprise migration path

The migration story is intentionally practical:
- keep orchestration unchanged,
- switch profile,
- plug in managed providers (OpenAI/Azure/Vertex + enterprise vector store + BigQuery).

That design reduces rewrite risk and accelerates enterprise hardening.

## Lessons learned

- "Working demo" is not "production-ready."  
- Semantic governance and observability are design-time decisions, not post-launch add-ons.  
- Hybrid retrieval is worth the extra complexity for enterprise content.

## Final takeaway

Enterprise AI assistants need **architecture discipline**, not just better prompts.  
This repository is a practical baseline for teams that need governed analytics copilots with real LLM and retrieval infrastructure.
