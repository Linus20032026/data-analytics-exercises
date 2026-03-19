# Exercise 8 — Staging models: products and orders

## Task
Write the SELECT statements in two more staging models.

**`dbt/models/staging/stg_products.sql`**
- Read from `bronze.products`.
- `TRIM()` all text columns.
- Cast `list_price::NUMERIC`.
- Filter: `WHERE product_id IS NOT NULL`.
- Expose: `product_id`, `product_name`, `category`, `subcategory`, `list_price`.

**`dbt/models/staging/stg_orders.sql`**
- Read from `bronze.orders`.
- `TRIM()` text columns: `order_id`, `client_id`, `product_id`.
- Cast columns:
  - `order_date::DATE`
  - `quantity::INTEGER`
  - `unit_price::NUMERIC`
  - `discount_pct::NUMERIC`
- Filter: `WHERE order_id IS NOT NULL AND order_date IS NOT NULL`.
- Expose all seven columns.

## Goal
Learn how to apply type casting in the staging layer. Downstream dbt
models can then do arithmetic (`quantity * unit_price`) without explicit
casts in every query.

## What is needed
- Exercise 7 completed (regions and clients staging done).
- Files to edit:
  - `dbt/models/staging/stg_products.sql`
  - `dbt/models/staging/stg_orders.sql`
- Verification — confirm the casts worked:
  ```sql
  SELECT pg_typeof(list_price) FROM silver.stg_products LIMIT 1;
  -- expected: numeric

  SELECT pg_typeof(order_date), pg_typeof(quantity)
  FROM silver.stg_orders LIMIT 1;
  -- expected: date, integer
  ```
