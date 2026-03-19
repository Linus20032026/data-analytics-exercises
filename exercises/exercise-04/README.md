# Exercise 4 — Load clients and products into the bronze layer

## Task
In `dags/etl_pipeline.py`, implement `load_clients()` and `load_products()`
by calling the `_load_csv()` helper you wrote in Exercise 3.

```
Clients  → table="clients",  csv="/opt/data/raw/clients.csv"
           columns: client_id, client_name, client_type, region_id, email

Products → table="products", csv="/opt/data/raw/products.csv"
           columns: product_id, product_name, category, subcategory, list_price
```

Trigger the DAG and verify the two new tasks turn green alongside `load_regions`.

## Goal
Practise reusing a helper function to ingest multiple tables with
minimal code. Notice that `_load_csv` handles both the DDL (`CREATE TABLE`)
and the load in one call, making each task a single line.

## What is needed
- Exercise 3 completed (`_load_csv()` implemented).
- File to edit: `dags/etl_pipeline.py`
- Verification queries:
  ```sql
  SELECT COUNT(*) FROM bronze.clients;
  SELECT COUNT(*) FROM bronze.products;
  ```
