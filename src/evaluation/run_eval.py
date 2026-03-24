<<<<<<< HEAD
"""Evaluation runner for route and grounding quality."""
from __future__ import annotations

from statistics import mean

=======
>>>>>>> main
from src.evaluation.dataset import BENCHMARK_QUESTIONS
from src.evaluation.judge import grounding_keyword_score


def run_eval(predict_fn):
    rows = []
    for item in BENCHMARK_QUESTIONS:
        result = predict_fn(item["question"])
<<<<<<< HEAD
        rows.append(
            {
                "question": item["question"],
                "route_match": float(result.get("route") == item["expected_route"]),
                "grounding_keyword_score": grounding_keyword_score(result.get("answer", ""), item["keywords"]),
            }
        )
    return rows


def summarize_eval(rows: list[dict]) -> dict:
    if not rows:
        return {"num_questions": 0, "route_accuracy": 0.0, "grounding_score": 0.0}
    return {
        "num_questions": len(rows),
        "route_accuracy": mean(r["route_match"] for r in rows),
        "grounding_score": mean(r["grounding_keyword_score"] for r in rows),
    }


if __name__ == "__main__":
    demo_rows = run_eval(lambda q: {"route": "mixed", "answer": "Texas sales grounded answer"})
    print(demo_rows)
    print(summarize_eval(demo_rows))
=======
        rows.append({
            "question": item["question"],
            "route_match": float(result.get("route") == item["expected_route"]),
            "grounding_keyword_score": grounding_keyword_score(result.get("answer", ""), item["keywords"]),
        })
    return rows
>>>>>>> main
