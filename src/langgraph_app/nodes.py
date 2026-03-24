<<<<<<< HEAD
"""Workflow nodes for multi-source analytics QA."""
from __future__ import annotations

import time
from typing import Any

from src.langgraph_app.tools import choose_route, draft_sql, evidence_validate, extract_entities_simple


def plan(state: dict[str, Any]) -> dict[str, Any]:
    state["route"] = choose_route(state["question"])
    state.setdefault("diagnostics", {})["planned_at"] = time.time()
    return state


def extract_entities(state: dict[str, Any]) -> dict[str, Any]:
=======
from src.langgraph_app.tools import choose_route, draft_sql, evidence_validate, extract_entities_simple


def plan(state: dict) -> dict:
    state["route"] = choose_route(state["question"])
    return state


def extract_entities(state: dict) -> dict:
>>>>>>> main
    state["entities"] = extract_entities_simple(state["question"])
    return state


<<<<<<< HEAD
def prepare_sql(state: dict[str, Any]) -> dict[str, Any]:
=======
def prepare_sql(state: dict) -> dict:
>>>>>>> main
    if state["route"] in {"structured", "mixed"}:
        state["sql"] = draft_sql(state["entities"])
    return state


<<<<<<< HEAD
def run_sql(state: dict[str, Any], sql_runner, access_ctx) -> dict[str, Any]:
    if state.get("sql"):
        start = time.perf_counter()
        state["sql_result"] = sql_runner.run(state["sql"], access_ctx).to_dict(orient="records")
        state.setdefault("diagnostics", {})["sql_latency_ms"] = round((time.perf_counter() - start) * 1000, 2)
    return state


def retrieve_docs(state: dict[str, Any], retriever, filters: dict[str, Any] | None) -> dict[str, Any]:
    if state["route"] in {"doc", "mixed"}:
        start = time.perf_counter()
        hits = retriever.retrieve(state["question"], top_k=8, filters=filters)
        state["docs"] = [d.__dict__ for d in hits]
        state.setdefault("diagnostics", {})["retrieval_latency_ms"] = round((time.perf_counter() - start) * 1000, 2)
    return state


def validate_evidence(state: dict[str, Any]) -> dict[str, Any]:
    state["validation_notes"] = evidence_validate(state)
    state.setdefault("diagnostics", {})["validation_passed"] = len(state["validation_notes"]) == 0
    return state


def synthesize_answer(state: dict[str, Any], llm) -> dict[str, Any]:
    prompt = (
        f"Question: {state['question']}\n"
        f"Route: {state.get('route')}\n"
        f"Structured evidence: {state.get('sql_result')}\n"
        f"Document evidence: {state.get('docs')}\n"
        f"Validation notes: {state.get('validation_notes')}\n"
        "Provide a concise, grounded answer and call out confidence and caveats."
    )
    state["answer"] = llm.invoke(prompt, system_prompt="You are an enterprise analytics assistant. Never hallucinate evidence.")
=======
def run_sql(state: dict, sql_runner, access_ctx) -> dict:
    if state.get("sql"):
        state["sql_result"] = sql_runner.run(state["sql"], access_ctx).to_dict(orient="records")
    return state


def retrieve_docs(state: dict, retriever, filters: dict) -> dict:
    if state["route"] in {"doc", "mixed"}:
        state["docs"] = [d.__dict__ for d in retriever.retrieve(state["question"], top_k=5, filters=filters)]
    return state


def validate_evidence(state: dict) -> dict:
    state["validation_notes"] = evidence_validate(state)
    return state


def synthesize_answer(state: dict, llm) -> dict:
    prompt = f"Question: {state['question']}\nStructured: {state.get('sql_result')}\nDocs: {state.get('docs')}"
    state["answer"] = llm.invoke(prompt, system_prompt="Ground answers in evidence and cite caveats.")
>>>>>>> main
    return state
