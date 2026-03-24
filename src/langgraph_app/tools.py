<<<<<<< HEAD
"""Pure helper tools used by workflow nodes."""
from __future__ import annotations

import re
from typing import Any


def extract_entities_simple(question: str) -> dict[str, Any]:
    """Lightweight entity extraction for local/dev mode.

    In enterprise deployments this function can be replaced by an LLM tool-call extractor
    without changing downstream orchestration.
    """
    q = question.lower()
    region = "US-SOUTH" if any(x in q for x in ["texas", "tx", "dallas", "austin"]) else "US-WEST"
    metric = "net_sales" if "sales" in q else "return_rate" if "return" in q else "inventory_health"

    sku_match = re.findall(r"[A-Z]{3}-\d{3}", question.upper())
    promo_match = re.findall(r"P\d{3}", question.upper())
    return {
        "region": region,
        "metric": metric,
        "product_ids": sku_match,
        "promo_ids": promo_match,
    }


def choose_route(question: str) -> str:
    """Choose a route for structured/doc/mixed reasoning."""
    q = question.lower()
    asks_explanation = any(x in q for x in ["why", "recommend", "policy", "sop", "playbook", "how"])
    asks_kpi = any(x in q for x in ["sales", "kpi", "inventory", "promo", "returns", "trend"])

    if asks_explanation and asks_kpi:
        return "mixed"
    if asks_explanation:
        return "doc"
    if asks_kpi:
        return "structured"
    return "mixed"


def draft_sql(entities: dict[str, Any]) -> str:
    """Create SQL against only approved semantic views."""
    region = entities.get("region", "US-SOUTH")
    metric = entities.get("metric", "net_sales")

    if metric == "inventory_health":
        return (
            "SELECT date, region, business_unit, product_id, inventory_status, on_hand_units "
            "FROM semantic_inventory_health "
            f"WHERE region = '{region}' "
            "ORDER BY date DESC LIMIT 100"
        )
    if metric == "return_rate":
        return (
            "SELECT date, region, business_unit, return_rate "
            "FROM semantic_kpi_daily "
            f"WHERE region = '{region}' "
            "ORDER BY date DESC LIMIT 100"
        )

    return (
        "SELECT date, region, business_unit, total_net_sales "
        "FROM semantic_kpi_daily "
        f"WHERE region = '{region}' "
        "ORDER BY date DESC LIMIT 100"
    )


def evidence_validate(state: dict[str, Any]) -> list[str]:
    """Validate evidence completeness and consistency before synthesis."""
    notes: list[str] = []
    route = state.get("route")
    sql_rows = state.get("sql_result") or []
    docs = state.get("docs") or []

    if route in {"structured", "mixed"} and not sql_rows:
        notes.append("No structured evidence available for the requested scope.")
    if route in {"doc", "mixed"} and not docs:
        notes.append("No policy/doc evidence available after access filtering.")

    entity_region = (state.get("entities") or {}).get("region")
    if entity_region and sql_rows:
        if any(row.get("region") and row.get("region") != entity_region for row in sql_rows):
            notes.append("Structured evidence contains mixed regions outside extracted scope.")

    if route == "doc" and docs and all(d.get("score", 0) < 0.05 for d in docs):
        notes.append("Retrieved documents are low-confidence; answer should be cautious.")

=======
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
>>>>>>> main
    return notes
