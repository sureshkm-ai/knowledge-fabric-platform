import re


def extract_entities_simple(question: str) -> dict:
    region = "US-SOUTH" if "texas" in question.lower() or "tx" in question.lower() else "US-WEST"
    return {"region": region, "kpi": "net_sales" if "sales" in question.lower() else "inventory"}


def choose_route(question: str) -> str:
    q = question.lower()
    if any(x in q for x in ["why", "policy", "sop", "playbook"]):
        return "doc"
    if any(x in q for x in ["sales", "kpi", "inventory", "promo"]):
        return "mixed"
    return "structured"


def draft_sql(entities: dict) -> str:
    return (
        "SELECT date, region, business_unit, total_net_sales "
        "FROM semantic_kpi_daily WHERE region = '{region}' ORDER BY date DESC LIMIT 30"
    ).format(region=entities.get("region", "US-SOUTH"))


def evidence_validate(state: dict) -> list[str]:
    notes = []
    if not state.get("sql_result") and state.get("route") in {"structured", "mixed"}:
        notes.append("No structured evidence")
    if not state.get("docs") and state.get("route") in {"doc", "mixed"}:
        notes.append("No unstructured evidence")
    return notes
