"""Strict SQL guardrails for semantic-layer-only querying."""
from __future__ import annotations

import re

APPROVED_OBJECTS = {
    "semantic_sales_daily",
    "semantic_sales_enriched",
    "semantic_inventory_health",
    "semantic_promo_effectiveness",
    "semantic_kpi_daily",
    "semantic_metric_dictionary",
}

DENYLIST_TOKENS = [
    "insert ",
    "update ",
    "delete ",
    "create ",
    "drop ",
    "alter ",
    "truncate ",
    "grant ",
    "revoke ",
    "copy ",
    "attach ",
]


def _extract_objects(sql: str) -> list[str]:
    return re.findall(r"(?:from|join)\s+([a-zA-Z0-9_\.]+)", sql)


def validate_sql(sql: str, max_limit: int = 1000, require_limit: bool = True) -> tuple[bool, str]:
    text = re.sub(r"\s+", " ", sql.strip().lower())
    if not text.startswith("select "):
        return False, "only SELECT statements are permitted"
    if any(token in text for token in DENYLIST_TOKENS):
        return False, "DDL/DML/admin statements are not permitted"
    if ";" in text[:-1]:
        return False, "multiple statements are not permitted"

    objects = [obj.split(".")[-1] for obj in _extract_objects(text)]
    disallowed = [obj for obj in objects if obj not in APPROVED_OBJECTS]
    if disallowed:
        return False, f"unapproved semantic objects detected: {sorted(set(disallowed))}"

    if "select *" in text:
        return False, "SELECT * is not permitted; enumerate columns"

    limit_match = re.search(r"\blimit\s+(\d+)\b", text)
    if require_limit and not limit_match:
        return False, "LIMIT is required"
    if limit_match and int(limit_match.group(1)) > max_limit:
        return False, f"LIMIT exceeds maximum of {max_limit}"

    return True, "ok"
