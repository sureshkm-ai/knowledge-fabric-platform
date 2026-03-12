"""Hybrid retriever that fuses vector and lexical retrieval."""
from __future__ import annotations

from src.retrieval.bm25_retriever import BM25Retriever
from src.retrieval.reranker import simple_rerank
from src.retrieval.vector_retriever import VectorRetriever
from src.vectorstore.base import RetrievedDoc


class HybridRetriever:
    def __init__(self, vector_retriever: VectorRetriever, bm25_retriever: BM25Retriever):
        self.vector_retriever = vector_retriever
        self.bm25_retriever = bm25_retriever

    def retrieve(self, query: str, top_k: int = 5, filters: dict | None = None) -> list[RetrievedDoc]:
        vec = self.vector_retriever.retrieve(query, top_k=top_k * 2, filters=filters)
        lex = self.bm25_retriever.retrieve(query, top_k=top_k * 2, filters=filters)

        fused: dict[str, RetrievedDoc] = {}
        for d in vec + lex:
            if d.doc_id in fused:
                fused[d.doc_id].score += d.score
            else:
                fused[d.doc_id] = RetrievedDoc(d.doc_id, d.text, d.score, d.metadata)

        return simple_rerank(query, list(fused.values()))[:top_k]
