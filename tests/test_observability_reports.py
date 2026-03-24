from pathlib import Path

from src.observability.logger import ObservabilityLogger
from src.observability.reports import summarize_trace


def test_trace_summary(tmp_path: Path):
    log_path = tmp_path / "trace.jsonl"
    logger = ObservabilityLogger(path=str(log_path))
    trace_id = "t1"
    logger.log(trace_id, "question_received", {"question": "q"})
    logger.log(trace_id, "answer_generated", {"route": "mixed", "validation": []})

    summary = summarize_trace(trace_id, path=str(log_path))
    assert summary.event_count == 2
    assert summary.route == "mixed"
