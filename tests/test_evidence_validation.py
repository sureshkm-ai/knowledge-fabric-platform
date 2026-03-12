from src.langgraph_app.tools import evidence_validate


def test_evidence_validation_flags_missing():
    notes = evidence_validate({"route": "mixed", "sql_result": [], "docs": []})
    assert "No structured evidence" in notes
    assert "No unstructured evidence" in notes
