"""Generate synthetic retail/CPG warehouse CSVs."""
from pathlib import Path
import random
import pandas as pd


def generate(output_dir: str = "data/raw", n_days: int = 30) -> None:
    random.seed(42)
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    days = pd.date_range("2024-01-01", periods=n_days)
    clubs = ["TX100", "TX200", "CA100"]
    products = ["SNK-001", "SNK-002", "BEV-001"]

    tx = []
    inv = []
    returns = []
    for d in days:
        for c in clubs:
            for p in products:
                units = random.randint(5, 120)
                price = random.choice([2.99, 4.99, 8.99])
                tx.append([d.date(), c, p, units, price, units * price, c[:2], "snacks" if "SNK" in p else "beverage"])
                inv.append([d.date(), c, p, random.randint(0, 500), c[:2], "snacks" if "SNK" in p else "beverage"])
                returns.append([d.date(), c, p, random.randint(0, 4), c[:2], "snacks" if "SNK" in p else "beverage"])

    pd.DataFrame(tx, columns=["date", "club_id", "product_id", "units", "unit_price", "net_sales", "region", "business_unit"]).to_csv(out / "transactions.csv", index=False)
    pd.DataFrame(inv, columns=["date", "club_id", "product_id", "on_hand_units", "region", "business_unit"]).to_csv(out / "inventory_snapshots.csv", index=False)
    pd.DataFrame(returns, columns=["date", "club_id", "product_id", "return_units", "region", "business_unit"]).to_csv(out / "returns.csv", index=False)

    pd.DataFrame([["SNK-001", "Chile Lime Chips", "snacks"], ["SNK-002", "Sea Salt Pretzels", "snacks"], ["BEV-001", "Sparkling Water", "beverage"]], columns=["product_id", "product_name", "category"]).to_csv(out / "product_master.csv", index=False)
    pd.DataFrame([["TX100", "Dallas North", "US-SOUTH"], ["TX200", "Austin Central", "US-SOUTH"], ["CA100", "San Diego", "US-WEST"]], columns=["club_id", "club_name", "region"]).to_csv(out / "club_master.csv", index=False)
    pd.DataFrame([["P001", "SNK-001", "BOGO", "2024-01-10", "2024-01-15"], ["P002", "SNK-002", "DISPLAY", "2024-01-20", "2024-01-27"]], columns=["promo_id", "product_id", "promo_type", "start_date", "end_date"]).to_csv(out / "promotions.csv", index=False)
    pd.DataFrame([["net_sales", "Sum of units * unit_price, excluding returns"], ["sell_through", "units sold divided by units available"], ["return_rate", "returned units / sold units"]], columns=["metric_name", "definition"]).to_csv(out / "metric_dictionary.csv", index=False)


if __name__ == "__main__":
    generate()
