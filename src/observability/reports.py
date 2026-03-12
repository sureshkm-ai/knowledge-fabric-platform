import json
from pathlib import Path


def read_trace(trace_id: str, path: str = "logs/traces.jsonl") -> list[dict]:
    p = Path(path)
    if not p.exists():
        return []
    out = []
    for line in p.read_text().splitlines():
        row = json.loads(line)
        if row["trace_id"] == trace_id:
            out.append(row)
    return out
