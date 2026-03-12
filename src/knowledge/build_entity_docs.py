import pandas as pd
from pathlib import Path


def build_entity_docs(raw_dir: str = "data/raw", output: str = "data/knowledge/entity_docs.jsonl") -> None:
    products = pd.read_csv(f"{raw_dir}/product_master.csv")
    clubs = pd.read_csv(f"{raw_dir}/club_master.csv")
    Path(output).parent.mkdir(parents=True, exist_ok=True)
    rows = []
    for _, p in products.iterrows():
        rows.append({"doc_id": f"product::{p.product_id}", "text": f"{p.product_name} is in {p.category}", "metadata": {"type": "product"}})
    for _, c in clubs.iterrows():
        rows.append({"doc_id": f"club::{c.club_id}", "text": f"{c.club_name} serves region {c.region}", "metadata": {"type": "club", "region": c.region}})
    pd.DataFrame(rows).to_json(output, orient="records", lines=True)
