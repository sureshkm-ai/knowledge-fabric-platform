from src.vectorstore.base import RetrievedDoc


def simple_rerank(query: str, docs: list[RetrievedDoc]) -> list[RetrievedDoc]:
    q_tokens = set(query.lower().split())
    rescored = []
    for doc in docs:
        overlap = len(q_tokens.intersection(set(doc.text.lower().split())))
        rescored.append(RetrievedDoc(doc.doc_id, doc.text, doc.score + 0.05 * overlap, doc.metadata))
    return sorted(rescored, key=lambda d: d.score, reverse=True)
