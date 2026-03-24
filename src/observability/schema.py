"""Structured observability event schemas."""
from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class TraceEvent(BaseModel):
    trace_id: str
    event_type: str
    payload: dict[str, Any] = Field(default_factory=dict)
    ts: float


class TraceSummary(BaseModel):
    trace_id: str
    event_count: int
    route: str | None = None
    validation_notes: list[str] = Field(default_factory=list)
    total_latency_ms: float | None = None
