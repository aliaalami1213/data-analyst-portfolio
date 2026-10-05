"""Build ecommerce.db (SQLite) from the project 4 CSV, then run every query in queries/.

Usage:  python build_db.py
Output: ecommerce.db (git-ignored) and one CSV per query in results/
"""
import sqlite3
from pathlib import Path

import pandas as pd

HERE = Path(__file__).parent
CSV = HERE.parent / "04-ecommerce-customer-segmentation" / "data" / "E-commerce_Customer_Segmentation_2026.csv"
DB = HERE / "ecommerce.db"

DB.unlink(missing_ok=True)
con = sqlite3.connect(DB)

# Load the raw file untouched into a staging table; all modeling happens in SQL.
pd.read_csv(CSV).to_sql("stg_customers", con, index=False)
con.executescript((HERE / "schema.sql").read_text())

for path in sorted((HERE / "queries").glob("*.sql")):
    result = pd.read_sql_query(path.read_text(), con)
    result.to_csv(HERE / "results" / f"{path.stem}.csv", index=False)
    print(f"\n-- {path.name}\n{result.to_string(index=False)}")

con.close()
