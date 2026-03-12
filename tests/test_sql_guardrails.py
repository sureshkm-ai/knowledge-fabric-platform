from src.agents.sql_guardrails import validate_sql


def test_blocks_raw_table_access():
    ok, _ = validate_sql("SELECT * FROM transactions LIMIT 10")
    assert not ok


def test_allows_semantic_view():
    ok, _ = validate_sql("SELECT * FROM semantic_kpi_daily LIMIT 10")
    assert ok
