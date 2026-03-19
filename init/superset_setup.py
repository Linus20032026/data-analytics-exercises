"""
Superset Dashboard Bootstrap
-----------------------------
Runs after `superset init` to auto-create:
  1. PostgreSQL database connection
  2. Virtual dataset (flat JOIN across all mart tables)
  3. Five charts
  4. One "Sales Analytics Dashboard"

Idempotent — tries to create each resource; if creation fails with a
duplicate error, falls back to listing all and finding by name.
"""

import os
import sys
import time
import json
import requests

# ── Config ────────────────────────────────────────────────────────────────────
SUPERSET_URL  = os.environ.get("SUPERSET_URL",  "http://localhost:8088")
SUPERSET_USER = os.environ.get("SUPERSET_USER", "admin")
SUPERSET_PASS = os.environ.get("SUPERSET_PASS", "admin")

PG_HOST = os.environ.get("ANALYTICS_DB_HOST",     "postgres")
PG_DB   = os.environ.get("ANALYTICS_DB_NAME",     "analytics_demo")
PG_USER = os.environ.get("ANALYTICS_DB_USER",     "admin")
PG_PASS = os.environ.get("ANALYTICS_DB_PASSWORD", "admin")
PG_PORT = int(os.environ.get("ANALYTICS_DB_PORT", "5432"))

VIRTUAL_SQL = """
SELECT
    f.sale_key,
    f.quantity,
    f.unit_price,
    f.discount_pct,
    f.total_amount,
    d.full_date,
    d.day,
    d.month,
    d.month_name,
    d.quarter,
    d.year,
    d.day_name,
    d.is_weekend,
    r.region_name,
    r.country,
    r.continent,
    c.client_name,
    c.client_type,
    c.email,
    p.product_name,
    p.category,
    p.subcategory,
    p.list_price
FROM gold.fact_sales f
JOIN gold.dim_date    d ON f.date_key    = d.date_key
JOIN gold.dim_region  r ON f.region_key  = r.region_key
JOIN gold.dim_client  c ON f.client_key  = c.client_key
JOIN gold.dim_product p ON f.product_key = p.product_key
""".strip()


# ── HTTP helpers ───────────────────────────────────────────────────────────────

class SupersetClient:
    def __init__(self):
        self.s    = requests.Session()
        self.base = SUPERSET_URL
        self._login()

    def _login(self):
        r = self.s.post(f"{self.base}/api/v1/security/login", json={
            "username": SUPERSET_USER,
            "password": SUPERSET_PASS,
            "provider": "db",
            "refresh":  True,
        })
        r.raise_for_status()
        token = r.json()["access_token"]
        self.s.headers.update({
            "Authorization": f"Bearer {token}",
            "Content-Type":  "application/json",
        })
        csrf = self.s.get(f"{self.base}/api/v1/security/csrf_token/")
        csrf.raise_for_status()
        self.s.headers["X-CSRFToken"] = csrf.json()["result"]

    def post(self, path, payload):
        r = self.s.post(f"{self.base}{path}", json=payload)
        return r

    def get_list(self, path):
        r = self.s.get(f"{self.base}{path}")
        r.raise_for_status()
        return r.json().get("result", [])

    def put(self, path, payload):
        r = self.s.put(f"{self.base}{path}", json=payload)
        r.raise_for_status()
        return r.json()


def find_by_name(items, name_field, name):
    return next((i for i in items if i.get(name_field) == name), None)


# ── Wait for Superset ─────────────────────────────────────────────────────────

def wait_for_superset(retries=30, delay=10):
    print("Waiting for Superset …", flush=True)
    for i in range(retries):
        try:
            r = requests.get(f"{SUPERSET_URL}/health", timeout=5)
            if r.status_code == 200:
                print("Superset is up.", flush=True)
                return
        except Exception:
            pass
        print(f"  [{i+1}/{retries}] not ready, retrying in {delay}s …", flush=True)
        time.sleep(delay)
    sys.exit("Superset did not become ready in time.")


# ── Step 1: Database connection ───────────────────────────────────────────────

def ensure_database(c: SupersetClient) -> int:
    all_dbs = c.get_list("/api/v1/database/")
    existing = find_by_name(all_dbs, "database_name", "analytics_demo")
    if existing:
        print(f"  Database already exists (id={existing['id']})", flush=True)
        return existing["id"]

    r = c.post("/api/v1/database/", {
        "database_name":    "analytics_demo",
        "sqlalchemy_uri":   f"postgresql+psycopg2://{PG_USER}:{PG_PASS}@{PG_HOST}:{PG_PORT}/{PG_DB}",
        "expose_in_sqllab": True,
    })
    if not r.ok:
        print(f"  Database create error {r.status_code}: {r.text[:400]}", flush=True)
        # Try to find it anyway (race condition or already exists)
        all_dbs = c.get_list("/api/v1/database/")
        existing = find_by_name(all_dbs, "database_name", "analytics_demo")
        if existing:
            return existing["id"]
        r.raise_for_status()

    db_id = r.json()["id"]
    print(f"  Created database connection (id={db_id})", flush=True)
    return db_id


# ── Step 2: Virtual dataset ───────────────────────────────────────────────────

def ensure_dataset(c: SupersetClient, db_id: int) -> int:
    all_ds = c.get_list("/api/v1/dataset/")
    existing = find_by_name(all_ds, "table_name", "sales_analytics")
    if existing:
        print(f"  Dataset already exists (id={existing['id']})", flush=True)
        return existing["id"]

    r = c.post("/api/v1/dataset/", {
        "database":   db_id,
        "schema":     "gold",
        "table_name": "sales_analytics",
        "sql":        VIRTUAL_SQL,
    })
    if not r.ok:
        body = r.text
        if "does not exist" in body or "Fatal error" in body:
            raise MartTablesNotReady("mart tables not yet populated — ETL pipeline has not run")
        all_ds = c.get_list("/api/v1/dataset/")
        existing = find_by_name(all_ds, "table_name", "sales_analytics")
        if existing:
            return existing["id"]
        print(f"  Dataset create failed: {r.status_code} {body[:300]}", flush=True)
        r.raise_for_status()

    ds_id = r.json()["id"]
    print(f"  Created virtual dataset (id={ds_id})", flush=True)
    return ds_id


class MartTablesNotReady(Exception):
    pass


# ── Step 3: Charts ────────────────────────────────────────────────────────────

CHARTS = [
    {
        "slice_name": "Total Revenue",
        "viz_type":   "big_number_total",
        "params": {
            "metric":        {"expressionType": "SIMPLE", "column": {"column_name": "total_amount"}, "aggregate": "SUM"},
            "subheader":     "All-time revenue",
            "y_axis_format": "$,.0f",
        },
    },
    {
        "slice_name": "Monthly Revenue Trend",
        "viz_type":   "echarts_timeseries_line",
        "params": {
            "x_axis":           "full_date",
            "time_grain_sqla":  "P1M",
            "metrics":          [{"expressionType": "SIMPLE", "column": {"column_name": "total_amount"}, "aggregate": "SUM", "label": "Revenue"}],
            "y_axis_format":    "$,.0f",
        },
    },
    {
        "slice_name": "Revenue by Region",
        "viz_type":   "echarts_bar",
        "params": {
            "metrics":       [{"expressionType": "SIMPLE", "column": {"column_name": "total_amount"}, "aggregate": "SUM", "label": "Revenue"}],
            "groupby":       ["region_name"],
            "y_axis_format": "$,.0f",
            "order_desc":    True,
        },
    },
    {
        "slice_name": "Revenue by Category",
        "viz_type":   "pie",
        "params": {
            "metric":      {"expressionType": "SIMPLE", "column": {"column_name": "total_amount"}, "aggregate": "SUM"},
            "groupby":     ["category"],
            "donut":       True,
            "show_labels": True,
        },
    },
    {
        "slice_name": "Top 10 Clients",
        "viz_type":   "table",
        "params": {
            "metrics":    [{"expressionType": "SIMPLE", "column": {"column_name": "total_amount"}, "aggregate": "SUM", "label": "Total Revenue"}],
            "groupby":    ["client_name", "client_type"],
            "order_desc": True,
            "row_limit":  10,
        },
    },
]


def ensure_charts(c: SupersetClient, ds_id: int) -> list:
    all_charts = c.get_list("/api/v1/chart/")
    chart_ids  = []

    for chart in CHARTS:
        existing = find_by_name(all_charts, "slice_name", chart["slice_name"])
        if existing:
            print(f"  Chart '{chart['slice_name']}' already exists (id={existing['id']})", flush=True)
            chart_ids.append(existing["id"])
            continue

        r = c.post("/api/v1/chart/", {
            "slice_name":      chart["slice_name"],
            "viz_type":        chart["viz_type"],
            "datasource_id":   ds_id,
            "datasource_type": "table",
            "params":          json.dumps(chart["params"]),
        })
        if not r.ok:
            print(f"  Chart '{chart['slice_name']}' failed: {r.status_code} {r.text[:200]}", flush=True)
            continue
        cid = r.json()["id"]
        print(f"  Created chart '{chart['slice_name']}' (id={cid})", flush=True)
        chart_ids.append(cid)

    return chart_ids


# ── Step 4: Dashboard ─────────────────────────────────────────────────────────

def ensure_dashboard(c: SupersetClient, chart_ids: list) -> int:
    all_dashboards = c.get_list("/api/v1/dashboard/")
    existing = find_by_name(all_dashboards, "dashboard_title", "Sales Analytics Dashboard")
    if existing:
        print(f"  Dashboard already exists (id={existing['id']})", flush=True)
        return existing["id"]

    # Build simple grid: one row per chart (each 12 columns wide, 50 units tall)
    pos = {
        "DASHBOARD_VERSION_KEY": "v2",
        "ROOT_ID": {"type": "ROOT", "id": "ROOT_ID", "children": ["GRID_ID"]},
        "GRID_ID": {"type": "GRID", "id": "GRID_ID", "children": [], "parents": ["ROOT_ID"]},
    }
    for i, cid in enumerate(chart_ids):
        row_id   = f"ROW-{i}"
        chart_id = f"CHART-{i}"
        pos["GRID_ID"]["children"].append(row_id)
        pos[row_id] = {
            "type": "ROW", "id": row_id,
            "children": [chart_id],
            "parents":  ["ROOT_ID", "GRID_ID"],
            "meta":     {"background": "BACKGROUND_TRANSPARENT"},
        }
        pos[chart_id] = {
            "type": "CHART", "id": chart_id,
            "children": [],
            "parents":  ["ROOT_ID", "GRID_ID", row_id],
            "meta":     {"chartId": cid, "width": 12, "height": 50},
        }

    r = c.post("/api/v1/dashboard/", {
        "dashboard_title": "Sales Analytics Dashboard",
        "published":       True,
        "position_json":   json.dumps(pos),
    })
    if not r.ok:
        print(f"  Dashboard create failed: {r.status_code} {r.text[:200]}", flush=True)
        r.raise_for_status()

    did = r.json()["id"]
    print(f"  Created dashboard (id={did})", flush=True)

    # Attach charts to dashboard
    c.s.post(
        f"{SUPERSET_URL}/api/v1/dashboard/{did}/charts",
        json={"chart_ids": chart_ids},
    )
    print(f"  Attached {len(chart_ids)} charts", flush=True)
    return did


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    wait_for_superset()

    print("\n[1/4] Authenticating …", flush=True)
    c = SupersetClient()
    print("      OK", flush=True)

    print("\n[2/4] Database connection …", flush=True)
    db_id = ensure_database(c)

    # Retry until the mart tables are populated by the Airflow ETL pipeline
    retry_delay = 60
    while True:
        try:
            print("\n[3/4] Virtual dataset …", flush=True)
            ds_id = ensure_dataset(c, db_id)
            break
        except MartTablesNotReady as e:
            print(f"  {e}", flush=True)
            print(f"  Retrying in {retry_delay}s — trigger the Airflow DAG etl_full_pipeline first.", flush=True)
            time.sleep(retry_delay)
            # Re-authenticate in case the token expired
            try:
                c = SupersetClient()
            except Exception:
                pass

    print("\n[4/4] Charts + Dashboard …", flush=True)
    chart_ids = ensure_charts(c, ds_id)
    did = ensure_dashboard(c, chart_ids)

    print(f"\nDone! Dashboard at http://localhost:8089/superset/dashboard/{did}/", flush=True)


if __name__ == "__main__":
    main()
