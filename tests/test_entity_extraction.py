from src.langgraph_app.tools import extract_entities_simple


def test_extract_entities_region():
    out = extract_entities_simple("Why are Texas snack sales down?")
    assert out["region"] == "US-SOUTH"
