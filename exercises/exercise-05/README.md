# Exercise 5 — Load orders into the bronze layer

## Task
In `dags/etl_pipeline.py`, implement `load_orders()`:

```
Orders → table="orders", csv="/opt/data/raw/orders.csv"
         columns: order_id, order_date, client_id, product_id,
                  quantity, unit_price, discount_pct
```

Trigger the DAG. All four `load_raw.*` tasks should now turn green.

## Goal
Complete the bronze layer. After this exercise the entire raw dataset
lives in PostgreSQL and every downstream layer (staging, silver, gold)
has data to work with. This milestone also confirms the Airflow task
group `load_raw` is fully wired up.

## What is needed
- Exercise 4 completed (clients and products loaded).
- File to edit: `dags/etl_pipeline.py`
- Verification queries:
  ```sql
  SELECT MIN(order_date), MAX(order_date), COUNT(*)
  FROM bronze.orders;
  ```
- After this exercise you should see all four bronze tables populated:
  `bronze.regions`, `bronze.clients`, `bronze.products`, `bronze.orders`.
