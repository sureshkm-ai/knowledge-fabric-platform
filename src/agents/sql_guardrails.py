<<<<<<< HEAD
"""Strict SQL guardrails for semantic-layer-only querying."""
from __future__ import annotations

=======
>>>>>>> main
import re

APPROVED_OBJECTS = {
    "semantic_sales_daily",
    "semantic_sales_enriched",
    "semantic_inventory_health",
    "semantic_promo_effectiveness",
    "semantic_kpi_daily",
    "semantic_metric_dictionary",
}

<<<<<<< HEAD
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

=======

def validate_sql(sql: str, max_limit: int = 1000) -> tuple[bool, str]:
    text = sql.strip().lower()
    if any(x in text for x in ["insert ", "update ", "delete ", "create ", "drop ", "alter ", "truncate "]):
        return False, "DDL/DML not permitted"
    if ";" in text[:-1]:
        return False, "multiple statements not permitted"
    tables = re.findall(r"from\s+([a-zA-Z0-9_\.]+)", text) + re.findall(r"join\s+([a-zA-Z0-9_\.]+)", text)
    bad = [t.split(".")[-1] for t in tables if t.split(".")[-1] not in APPROVED_OBJECTS]
    if bad:
        return False, f"unapproved objects: {bad}"
    lim = re.search(r"limit\s+(\d+)", text)
    if lim and int(lim.group(1)) > max_limit:
        return False, "limit too high"
>>>>>>> main
    return True, "ok"
