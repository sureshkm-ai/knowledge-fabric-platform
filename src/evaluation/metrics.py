import math


def precision_at_k(relevant: set[str], ranked: list[str], k: int) -> float:
    top = ranked[:k]
    return len([x for x in top if x in relevant]) / max(k, 1)


def recall_at_k(relevant: set[str], ranked: list[str], k: int) -> float:
    top = ranked[:k]
    return len([x for x in top if x in relevant]) / max(len(relevant), 1)


def mrr(relevant: set[str], ranked: list[str]) -> float:
    for i, item in enumerate(ranked, start=1):
        if item in relevant:
            return 1.0 / i
    return 0.0


def ndcg_at_k(relevant: set[str], ranked: list[str], k: int) -> float:
    dcg = 0.0
    for i, item in enumerate(ranked[:k], start=1):
        rel = 1 if item in relevant else 0
        dcg += rel / math.log2(i + 1)
    idcg = sum(1 / math.log2(i + 1) for i in range(1, min(len(relevant), k) + 1))
    return dcg / idcg if idcg else 0.0
