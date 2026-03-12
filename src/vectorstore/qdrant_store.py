from qdrant_client import QdrantClient

from src.vectorstore.base import BaseVectorStore, RetrievedDoc


class QdrantVectorStore(BaseVectorStore):
    def __init__(self, url: str, api_key: str | None = None, collection: str = "enterprise_docs"):
        self.client = QdrantClient(url=url, api_key=api_key)
        self.collection = collection

    def upsert(self, items: list[dict]) -> None:
        from qdrant_client.models import PointStruct

        points = [
            PointStruct(id=i["doc_id"], vector=i["vector"], payload={"text": i["text"], **i.get("metadata", {})})
            for i in items
        ]
        self.client.upsert(collection_name=self.collection, points=points)

    def query(self, vector: list[float], top_k: int = 5, filters: dict | None = None) -> list[RetrievedDoc]:
        hits = self.client.search(collection_name=self.collection, query_vector=vector, limit=top_k)
        out = []
        for h in hits:
            payload = h.payload or {}
            out.append(RetrievedDoc(str(h.id), payload.get("text", ""), float(h.score), payload))
        return out
