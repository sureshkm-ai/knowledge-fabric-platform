"""Public runner entrypoint for API and evaluation flows."""
from __future__ import annotations

from src.agents.sql_runner import SQLRunner
from src.config.provider_registry import create_runtime_components
from src.langgraph_app.graph import run_graph
from src.retrieval.bm25_retriever import BM25Retriever
from src.retrieval.hybrid_retriever import HybridRetriever
from src.retrieval.vector_retriever import VectorRetriever
from src.security.access_control import filter_docs_by_access
from src.security.policies import AccessContext


def ask_question(question: str, ctx: AccessContext, docs: list[dict]) -> dict:
    runtime = create_runtime_components()
    sql_runner = SQLRunner(runtime["settings"].profile.sql_backend, runtime["settings"].duckdb_path)

    scoped_docs = filter_docs_by_access(docs, ctx)
    vector = VectorRetriever(runtime["embeddings"], runtime["vectorstore"])
    bm25 = BM25Retriever(scoped_docs)
    retriever = HybridRetriever(vector, bm25)

    filters = {"region": ctx.allowed_regions[0]} if ctx.allowed_regions else None
    state = {"question": question, "diagnostics": {"profile": runtime["settings"].profile.name}}
    return run_graph(state, sql_runner, ctx, retriever, runtime["llm"], filters)
