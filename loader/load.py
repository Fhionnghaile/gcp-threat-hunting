"""Load synthetic audit logs into BigQuery (prod) or DuckDB (local/CI).

  python loader/load.py --duckdb hunt.db          # local, for testing hunts
  python loader/load.py --bq my_project.secops     # BigQuery (needs google-cloud-bigquery + creds)
"""
from __future__ import annotations
import argparse, json, pathlib

ROWS = [json.loads(l) for l in pathlib.Path("data/synthetic_audit.jsonl").read_text().splitlines() if l.strip()]
COLS = ["ts", "epoch_s", "actor", "action", "src_ip", "lat", "lng", "resource", "role_granted", "grantee"]

def to_duckdb(path: str):
    import duckdb
    con = duckdb.connect(path)
    con.execute("""CREATE OR REPLACE TABLE audit_log(
        ts TIMESTAMP, epoch_s BIGINT, actor TEXT, action TEXT, src_ip TEXT,
        lat DOUBLE, lng DOUBLE, resource TEXT, role_granted TEXT, grantee TEXT)""")
    con.executemany("INSERT INTO audit_log VALUES (" + ",".join("?" * len(COLS)) + ")",
                    [[r[c] for c in COLS] for r in ROWS])
    con.close()

def to_bq(table: str):
    from google.cloud import bigquery
    client = bigquery.Client()
    client.load_table_from_json(ROWS, table).result()

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--duckdb"); ap.add_argument("--bq")
    a = ap.parse_args()
    if a.duckdb: to_duckdb(a.duckdb); print(f"loaded {len(ROWS)} rows into DuckDB {a.duckdb}")
    elif a.bq: to_bq(a.bq); print(f"loaded {len(ROWS)} rows into BigQuery {a.bq}")
    else: ap.error("pass --duckdb PATH or --bq TABLE")
