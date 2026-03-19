# Exercise 3 — Load regions into the bronze layer

## Task
Open `dags/etl_pipeline.py` and implement two things:

**1. The helper `_load_csv(table, csv_path, columns)`**

Follow the steps in the docstring:
1. Use `glob.glob(csv_path)` to find matching files.
   Raise `FileNotFoundError` if the list is empty.
2. Open a psycopg2 connection using `DB_CONN`.
3. `CREATE TABLE IF NOT EXISTS bronze.<table>` where every column is `TEXT`.
4. `TRUNCATE` the table so re-runs are safe.
5. For each file: read with `csv.DictReader`, build a list of row tuples,
   insert with `cursor.executemany()`.
6. `conn.commit()` and close the connection.

**2. `load_regions()`**
```python
def load_regions():
    _load_csv(
        table    = "regions",
        csv_path = "/opt/data/raw/regions.csv",
        columns  = ["region_id", "region_name", "country", "continent"],
    )
```

Trigger the DAG in Airflow and verify only `load_raw.load_regions` turns green.

## Goal
Understand how raw CSV data is ingested into PostgreSQL using Python
and psycopg2. The bronze schema stores everything as TEXT — no types,
no cleaning — to preserve the original data exactly as it arrived.

## What is needed
- Exercise 2 completed (data understood).
- File to edit: `dags/etl_pipeline.py`
- Airflow at http://localhost:8088 to trigger and monitor the task.
- Verification query (run in psql or any SQL client):
  ```sql
  SELECT * FROM bronze.regions LIMIT 5;
  ```
- `psycopg2` is already installed in the Airflow container.
- `DB_CONN` dict and the `/opt/data/raw/` volume mount are pre-configured
  in `docker-compose.yml` — do not change them.
