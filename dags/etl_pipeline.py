"""
Full Data Warehouse ETL Pipeline
---------------------------------
Three-layer medallion architecture:

  [Group 1] Load Raw      → bronze schema  (CSV files → Postgres tables)
  [Group 2] Silver Layer   → silver schema  (dbt staging + silver models)
  [Group 3] Gold Layer     → gold schema    (dbt star schema: dims + fact)

Drop CSV files into ./data/raw/ and trigger this DAG manually or @daily.

Exercises 3–13 ask you to implement the functions below step by step.
"""

import os
import csv
import glob
import psycopg2
import requests
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.task_group import TaskGroup

# ---------------------------------------------------------------------------
# Connection config — reads from Docker environment variables (do not change)
# ---------------------------------------------------------------------------

DB_CONN = {
    "host":     os.environ["ANALYTICS_DB_HOST"],
    "dbname":   os.environ["ANALYTICS_DB_NAME"],
    "user":     os.environ["ANALYTICS_DB_USER"],
    "password": os.environ["ANALYTICS_DB_PASSWORD"],
}
DBT_BASE = "http://dbt:8087"


# ---------------------------------------------------------------------------
# Helper functions — Exercise 3
# ---------------------------------------------------------------------------

def _load_csv(table: str, csv_path: str, columns: list[str]):
    """
    Truncate and reload a bronze table from a CSV file.

    Steps to implement:
      1. Use glob.glob(csv_path) to find matching files — raise FileNotFoundError if none.
      2. Open a psycopg2 connection using DB_CONN.
      3. CREATE TABLE IF NOT EXISTS bronze.<table> with all columns as TEXT.
      4. TRUNCATE the table.
      5. For each file: read with csv.DictReader, INSERT all rows with executemany().
      6. Commit and close.
    """
    raise NotImplementedError("Exercise 3: implement _load_csv()")


def _call_dbt(endpoint: str):
    """
    POST to a dbt server endpoint and raise on failure.

    Steps to implement:
      1. POST to f"{DBT_BASE}/{endpoint}" with a 300s timeout.
      2. Parse the JSON response.
      3. Print result["output"].
      4. If result["returncode"] != 0, raise an Exception.
    """
    raise NotImplementedError("Exercise 6: implement _call_dbt()")


# ---------------------------------------------------------------------------
# Task functions — Group 1: Load Raw   (Exercises 3–5)
# ---------------------------------------------------------------------------

def load_regions():
    """Exercise 3: load data/raw/regions.csv → bronze.regions"""
    # Columns: region_id, region_name, country, continent
    raise NotImplementedError("Exercise 3: call _load_csv() for regions")


def load_clients():
    """Exercise 4: load data/raw/clients.csv → bronze.clients"""
    # Columns: client_id, client_name, client_type, region_id, email
    raise NotImplementedError("Exercise 4: call _load_csv() for clients")


def load_products():
    """Exercise 4: load data/raw/products.csv → bronze.products"""
    # Columns: product_id, product_name, category, subcategory, list_price
    raise NotImplementedError("Exercise 4: call _load_csv() for products")


def load_orders():
    """Exercise 5: load data/raw/orders.csv → bronze.orders"""
    # Columns: order_id, order_date, client_id, product_id, quantity, unit_price, discount_pct
    raise NotImplementedError("Exercise 5: call _load_csv() for orders")


# ---------------------------------------------------------------------------
# Task functions — Group 2: CDW Core   (Exercises 6–11)
# ---------------------------------------------------------------------------

def run_dbt_staging():
    """Exercise 6: trigger dbt staging models via the HTTP server"""
    # Hint: call _call_dbt() with the staging endpoint
    raise NotImplementedError("Exercise 6: call _call_dbt() for staging")


def run_dbt_silver():
    """Exercise 9: trigger dbt core models via the HTTP server"""
    raise NotImplementedError("Exercise 9: call _call_dbt() for silver")


# ---------------------------------------------------------------------------
# Task functions — Group 3: Data Mart  (Exercises 12–13)
# ---------------------------------------------------------------------------

def run_dbt_gold():
    """Exercise 12: trigger dbt mart models via the HTTP server"""
    raise NotImplementedError("Exercise 12: call _call_dbt() for gold")


# ---------------------------------------------------------------------------
# DAG definition — do not modify this section
# ---------------------------------------------------------------------------

with DAG(
    dag_id="etl_full_pipeline",
    description="CSV → bronze → Bronze → Silver → Gold Star Schema",
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",
    catchup=False,
) as dag:

    with TaskGroup("load_raw") as load_raw:
        t_regions  = PythonOperator(task_id="load_regions",  python_callable=load_regions)
        t_clients  = PythonOperator(task_id="load_clients",  python_callable=load_clients)
        t_products = PythonOperator(task_id="load_products", python_callable=load_products)
        t_orders   = PythonOperator(task_id="load_orders",   python_callable=load_orders)

    with TaskGroup("silver") as silver:
        t_staging = PythonOperator(task_id="run_dbt_staging", python_callable=run_dbt_staging)
        t_core    = PythonOperator(task_id="run_dbt_silver",    python_callable=run_dbt_silver)
        t_staging >> t_core

    with TaskGroup("gold") as gold:
        t_mart = PythonOperator(task_id="run_dbt_gold", python_callable=run_dbt_gold)

    load_raw >> silver >> gold
