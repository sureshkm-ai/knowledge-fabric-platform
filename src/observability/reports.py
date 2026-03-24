"""Trace reporting utilities."""
from __future__ import annotations

import json
from pathlib import Path

from src.observability.schema import TraceSummary


def read_trace(trace_id: str, path: str = "logs/traces.jsonl") -> list[dict]:
    p = Path(path)
    if not p.exists():
        return []

    out = []
    with p.open(encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            row = json.loads(line)
            if row.get("trace_id") == trace_id:
                out.append(row)
    return out


def summarize_trace(trace_id: str, path: str = "logs/traces.jsonl") -> TraceSummary:
    events = read_trace(trace_id, path)
    route = None
    validation_notes: list[str] = []
    if events:
        for e in events:
            payload = e.get("payload", {})
            route = payload.get("route", route)
            if "validation" in payload and isinstance(payload["validation"], list):
                validation_notes = payload["validation"]
        total_latency_ms = (events[-1]["ts"] - events[0]["ts"]) * 1000.0 if len(events) > 1 else 0.0
    else:
        total_latency_ms = None

    return TraceSummary(
        trace_id=trace_id,
        event_count=len(events),
        route=route,
        validation_notes=validation_notes,
        total_latency_ms=total_latency_ms,
    )
