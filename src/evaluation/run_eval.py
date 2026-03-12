from src.evaluation.dataset import BENCHMARK_QUESTIONS
from src.evaluation.judge import grounding_keyword_score


def run_eval(predict_fn):
    rows = []
    for item in BENCHMARK_QUESTIONS:
        result = predict_fn(item["question"])
        rows.append({
            "question": item["question"],
            "route_match": float(result.get("route") == item["expected_route"]),
            "grounding_keyword_score": grounding_keyword_score(result.get("answer", ""), item["keywords"]),
        })
    return rows
