import numpy as np

from src.vectorstore.base import BaseVectorStore, RetrievedDoc


class FaissVectorStore(BaseVectorStore):
    def __init__(self):
        self.items: list[dict] = []

    def upsert(self, items: list[dict]) -> None:
        self.items.extend(items)

    def query(self, vector: list[float], top_k: int = 5, filters: dict | None = None) -> list[RetrievedDoc]:
        if not self.items:
            return []
        q = np.array(vector)
        hits: list[RetrievedDoc] = []
        for item in self.items:
            if filters and any(item.get("metadata", {}).get(k) != v for k, v in filters.items()):
                continue
            v = np.array(item["vector"])
            score = float(np.dot(q, v) / (np.linalg.norm(q) * np.linalg.norm(v) + 1e-9))
            hits.append(RetrievedDoc(item["doc_id"], item["text"], score, item.get("metadata", {})))
        return sorted(hits, key=lambda x: x.score, reverse=True)[:top_k]
