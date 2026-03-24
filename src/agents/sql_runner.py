<<<<<<< HEAD
"""SQL execution adapter with guardrails + scoped filtering."""
from __future__ import annotations

=======
>>>>>>> main
import duckdb
import pandas as pd

from src.agents.sql_guardrails import validate_sql
from src.security.access_control import filter_sql_by_scope
from src.security.policies import AccessContext


class SQLRunner:
    def __init__(self, backend: str, conn_ref: str):
        self.backend = backend
        self.conn_ref = conn_ref

    def run(self, sql: str, ctx: AccessContext) -> pd.DataFrame:
        ok, msg = validate_sql(sql)
        if not ok:
<<<<<<< HEAD
            raise ValueError(f"SQL blocked by guardrails: {msg}")

=======
            raise ValueError(f"SQL blocked: {msg}")
>>>>>>> main
        scoped_sql = filter_sql_by_scope(sql, ctx)
        if self.backend == "duckdb":
            conn = duckdb.connect(self.conn_ref)
            try:
                return conn.sql(scoped_sql).to_df()
            finally:
                conn.close()
<<<<<<< HEAD

        if self.backend == "bigquery":
            raise NotImplementedError(
                "BigQuery backend should be supplied in enterprise runtime with a governed query service."
            )

        raise ValueError(f"Unsupported SQL backend: {self.backend}")
=======
        raise NotImplementedError("BigQuery execution should be implemented in enterprise runtime")
>>>>>>> main
