from src.evaluation.metrics import precision_at_k, recall_at_k, mrr, ndcg_at_k


def test_metrics():
    rel = {"a", "b"}
    ranked = ["a", "x", "b"]
    assert precision_at_k(rel, ranked, 2) == 0.5
    assert recall_at_k(rel, ranked, 3) == 1.0
    assert mrr(rel, ranked) == 1.0
    assert ndcg_at_k(rel, ranked, 3) > 0
