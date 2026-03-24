<<<<<<< HEAD
"""Qdrant vector-store integration."""
from __future__ import annotations

from qdrant_client import QdrantClient
from qdrant_client.models import FieldCondition, Filter, MatchValue, PointStruct
=======
from qdrant_client import QdrantClient
>>>>>>> main

from src.vectorstore.base import BaseVectorStore, RetrievedDoc


class QdrantVectorStore(BaseVectorStore):
    def __init__(self, url: str, api_key: str | None = None, collection: str = "enterprise_docs"):
        self.client = QdrantClient(url=url, api_key=api_key)
        self.collection = collection

    def upsert(self, items: list[dict]) -> None:
<<<<<<< HEAD
=======
        from qdrant_client.models import PointStruct

>>>>>>> main
        points = [
            PointStruct(id=i["doc_id"], vector=i["vector"], payload={"text": i["text"], **i.get("metadata", {})})
            for i in items
        ]
        self.client.upsert(collection_name=self.collection, points=points)

    def query(self, vector: list[float], top_k: int = 5, filters: dict | None = None) -> list[RetrievedDoc]:
<<<<<<< HEAD
        qdrant_filter = None
        if filters:
            conditions = []
            for key, value in filters.items():
                if isinstance(value, dict) and "in" in value:
                    conditions.extend(FieldCondition(key=key, match=MatchValue(value=v)) for v in value["in"])
                else:
                    conditions.append(FieldCondition(key=key, match=MatchValue(value=value)))
            qdrant_filter = Filter(should=conditions)

        hits = self.client.search(
            collection_name=self.collection,
            query_vector=vector,
            query_filter=qdrant_filter,
            limit=top_k,
        )
        return [RetrievedDoc(str(h.id), (h.payload or {}).get("text", ""), float(h.score), h.payload or {}) for h in hits]
=======
        hits = self.client.search(collection_name=self.collection, query_vector=vector, limit=top_k)
        out = []
        for h in hits:
            payload = h.payload or {}
            out.append(RetrievedDoc(str(h.id), payload.get("text", ""), float(h.score), payload))
        return out
>>>>>>> main
