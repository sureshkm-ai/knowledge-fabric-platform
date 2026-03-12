from rank_bm25 import BM25Okapi

from src.vectorstore.base import RetrievedDoc


class BM25Retriever:
    def __init__(self, docs: list[dict]):
        self.docs = docs
        self.tokenized = [d["text"].lower().split() for d in docs]
        self.model = BM25Okapi(self.tokenized) if docs else None

    def retrieve(self, query: str, top_k: int = 5, filters: dict | None = None) -> list[RetrievedDoc]:
        if not self.docs or self.model is None:
            return []
        scores = self.model.get_scores(query.lower().split())
        pairs = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)
        out = []
        for idx, score in pairs:
            doc = self.docs[idx]
            if filters and any(doc.get("metadata", {}).get(k) != v for k, v in filters.items()):
                continue
            out.append(RetrievedDoc(doc["doc_id"], doc["text"], float(score), doc.get("metadata", {})))
            if len(out) >= top_k:
                break
        return out
