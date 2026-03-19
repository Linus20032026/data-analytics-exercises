# Exercise 6 — Implement the dbt HTTP trigger and run staging

## Task
In `dags/etl_pipeline.py`, implement two things:

**1. `_call_dbt(endpoint)`**

Follow the steps in the docstring:
1. POST to `f"{DBT_BASE}/{endpoint}"` with `timeout=300`.
2. Parse the JSON response body.
3. `print(result["output"])` so the dbt log appears in Airflow task logs.
4. If `result["returncode"] != 0`, raise an `Exception`.

**2. `run_dbt_staging()`**
```python
def run_dbt_staging():
    _call_dbt("run/staging")
```

Test the dbt endpoint directly before running in Airflow:
```bash
curl -X POST http://localhost:8087/run/staging
```
You will get `returncode: 1` because the staging SQL is not written yet —
that confirms the endpoint is reachable.

## Goal
Learn how Airflow communicates with the separate dbt container via HTTP.
dbt runs in its own Docker service (`dbt/server.py`) to avoid Python
dependency conflicts with Airflow. The `_call_dbt()` helper bridges them.

## What is needed
- Exercise 5 completed (all bronze tables loaded).
- File to edit: `dags/etl_pipeline.py`
- `DBT_BASE = "http://dbt:8087"` is already defined — do not change it.
- Available dbt endpoints:
  - `POST /run/staging` — runs models tagged `staging`
  - `POST /run/silver`  — runs models tagged `silver`
  - `POST /run/gold`    — runs models tagged `gold`
  - `GET  /health`      — liveness check
