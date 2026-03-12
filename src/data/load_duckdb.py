from pathlib import Path
import duckdb

from src.data.generate_synthetic_data import generate


def load(db_path: str = "data/local_warehouse.duckdb", raw_dir: str = "data/raw") -> None:
    if not Path(raw_dir).exists():
        generate(raw_dir)
    conn = duckdb.connect(db_path)
    for t in ["transactions", "inventory_snapshots", "promotions", "product_master", "club_master", "returns", "metric_dictionary"]:
        conn.sql(f"CREATE OR REPLACE TABLE {t} AS SELECT * FROM read_csv_auto('{raw_dir}/{t}.csv', header=true)")
    semantic_sql = Path("src/data/semantic_views.sql").read_text()
    conn.execute(semantic_sql)
    conn.close()


if __name__ == "__main__":
    load()
