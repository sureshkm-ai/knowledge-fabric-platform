import re

APPROVED_OBJECTS = {
    "semantic_sales_daily",
    "semantic_sales_enriched",
    "semantic_inventory_health",
    "semantic_promo_effectiveness",
    "semantic_kpi_daily",
    "semantic_metric_dictionary",
}


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
    return True, "ok"
