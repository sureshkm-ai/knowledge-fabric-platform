<<<<<<< HEAD
"""State contracts for the analytics agent workflow."""
from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


RouteType = Literal["structured", "doc", "mixed"]


class AgentState(BaseModel):
    """Canonical state shared by all workflow stages."""

    question: str
    trace_id: str | None = None
    route: RouteType = "mixed"
    entities: dict[str, Any] = Field(default_factory=dict)

    sql: str | None = None
    sql_result: list[dict[str, Any]] = Field(default_factory=list)

    docs: list[dict[str, Any]] = Field(default_factory=list)
    validation_notes: list[str] = Field(default_factory=list)

    answer: str | None = None
    diagnostics: dict[str, Any] = Field(default_factory=dict)
=======
from pydantic import BaseModel
from typing import Any


class AgentState(BaseModel):
    question: str
    route: str = "mixed"
    entities: dict[str, Any] = {}
    sql: str | None = None
    sql_result: list[dict] = []
    docs: list[dict] = []
    validation_notes: list[str] = []
    answer: str | None = None
>>>>>>> main
