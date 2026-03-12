from pydantic import BaseModel
from typing import Any


class TraceEvent(BaseModel):
    trace_id: str
    event_type: str
    payload: dict[str, Any]
    ts: float
