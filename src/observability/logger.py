import json
import time
from pathlib import Path
from uuid import uuid4

from src.observability.schema import TraceEvent


class ObservabilityLogger:
    def __init__(self, backend: str = "jsonl", path: str = "logs/traces.jsonl"):
        self.backend = backend
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def new_trace_id(self) -> str:
        return str(uuid4())

    def log(self, trace_id: str, event_type: str, payload: dict):
        event = TraceEvent(trace_id=trace_id, event_type=event_type, payload=payload, ts=time.time())
        if self.backend == "jsonl":
            with self.path.open("a") as f:
                f.write(event.model_dump_json() + "\n")
        # enterprise adapter hooks (BigQuery / Cloud Logging) go here
