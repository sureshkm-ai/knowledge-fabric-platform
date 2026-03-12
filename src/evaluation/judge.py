def grounding_keyword_score(answer: str, keywords: list[str]) -> float:
    lower = answer.lower()
    return sum(1 for k in keywords if k.lower() in lower) / max(len(keywords), 1)
