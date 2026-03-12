"""Graph execution facade.

Uses an explicit staged pipeline that mirrors a LangGraph state machine.
If LangGraph is available at runtime, this module can be extended to compile a
native `StateGraph`; for deterministic local execution we keep a transparent path.
"""
from __future__ import annotations

from typing import Any

from src.langgraph_app import nodes


def run_graph(
    state: dict[str, Any],
    sql_runner,
    access_ctx,
    retriever,
    llm,
    filters: dict[str, Any] | None,
) -> dict[str, Any]:
    """Run the orchestrated workflow with explicit stage ordering."""
    state = nodes.plan(state)
    state = nodes.extract_entities(state)

    if state["route"] in {"structured", "mixed"}:
        state = nodes.prepare_sql(state)
        state = nodes.run_sql(state, sql_runner, access_ctx)

    if state["route"] in {"doc", "mixed"}:
        state = nodes.retrieve_docs(state, retriever, filters)

    state = nodes.validate_evidence(state)
    state = nodes.synthesize_answer(state, llm)
    return state
