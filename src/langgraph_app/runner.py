from src.config.provider_registry import create_runtime_components
from src.security.policies import AccessContext
from src.agents.sql_runner import SQLRunner
from src.retrieval.bm25_retriever import BM25Retriever
from src.retrieval.vector_retriever import VectorRetriever
from src.retrieval.hybrid_retriever import HybridRetriever
from src.langgraph_app.graph import run_graph


def ask_question(question: str, ctx: AccessContext, docs: list[dict]) -> dict:
    runtime = create_runtime_components()
    sql_runner = SQLRunner(runtime["settings"].profile.sql_backend, runtime["settings"].duckdb_path)
    vector = VectorRetriever(runtime["embeddings"], runtime["vectorstore"])
    bm25 = BM25Retriever(docs)
    retriever = HybridRetriever(vector, bm25)
    filters = {"region": ctx.allowed_regions[0]} if ctx.allowed_regions else None
    state = {"question": question}
    return run_graph(state, sql_runner, ctx, retriever, runtime["llm"], filters)
