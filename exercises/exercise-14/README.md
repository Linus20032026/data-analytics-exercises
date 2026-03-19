# Exercise 14 — Run the full Airflow pipeline end-to-end

## Task
In `dags/etl_pipeline.py`, implement the two remaining task functions:

```python
def run_dbt_silver():
    _call_dbt("run/silver")

def run_dbt_gold():
    _call_dbt("run/gold")
```

Then go to Airflow (http://localhost:8088) and trigger the full DAG
`etl_full_pipeline` manually. Watch all three task groups turn green:

```
load_raw ✓  →  silver ✓  →  gold ✓
```

If any task fails, click on it and open the **Log** tab — it will show
the exact Python traceback or dbt error message.

## Goal
Run the complete end-to-end pipeline through Airflow's UI for the first
time. This validates that every piece you built in Exercises 3–13 works
together as a single orchestrated workflow: CSV → bronze → silver → gold.

## What is needed
- Exercises 3–13 completed (all models and task functions implemented).
- File to edit: `dags/etl_pipeline.py` (add `run_dbt_silver` and `run_dbt_gold`).
- Airflow at http://localhost:8088.
- If the DAG is paused (grey toggle), click the toggle to unpause it
  before triggering.
- Post-run verification:
  ```sql
  SELECT COUNT(*) FROM gold.fact_sales;
  SELECT COUNT(*) FROM gold.dim_date;
  ```
  Both should be non-zero. The pipeline is idempotent — safe to re-trigger.
