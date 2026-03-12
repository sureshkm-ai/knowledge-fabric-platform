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
