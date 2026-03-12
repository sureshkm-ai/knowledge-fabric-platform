from src.agents.sql_guardrails import validate_sql


def test_blocks_raw_table_access():
    ok, msg = validate_sql("SELECT date FROM transactions LIMIT 10")
    assert not ok
    assert "unapproved" in msg


def test_blocks_select_star():
    ok, msg = validate_sql("SELECT * FROM semantic_kpi_daily LIMIT 10")
    assert not ok
    assert "SELECT *" in msg


def test_requires_limit():
    ok, msg = validate_sql("SELECT date FROM semantic_kpi_daily")
    assert not ok
    assert "LIMIT" in msg


def test_allows_semantic_view_with_columns():
    ok, _ = validate_sql("SELECT date, total_net_sales FROM semantic_kpi_daily LIMIT 10")
    assert ok
