# Exercise 13 — Gold layer: fact table

## Task
Open `dbt/models/gold/fact_sales.sql` and write the SELECT statement.

The fact table is a thin projection of `{{ ref('silver_orders') }}`:

| Output column  | Source column  | Note                        |
|----------------|----------------|-----------------------------|
| `sale_key`     | `order_sk`     | degenerate dimension / PK   |
| `date_key`     | `date_key`     | FK → `dim_date`             |
| `client_key`   | `client_sk`    | FK → `dim_client`           |
| `product_key`  | `product_sk`   | FK → `dim_product`          |
| `region_key`   | `region_sk`    | FK → `dim_region`           |
| `quantity`     | `quantity`     | measure                     |
| `unit_price`   | `unit_price`   | measure                     |
| `discount_pct` | `discount_pct` | measure                     |
| `total_amount` | `total_amount` | pre-computed revenue measure|

No joins needed — all keys and measures are already in `silver_orders`.

## Goal
Complete the star schema. `fact_sales` is the centre table that
BI tools (Superset, Tableau, Power BI) query by joining to the four
dimension tables. Keeping it narrow and pre-computed makes dashboard
queries fast and simple.

## What is needed
- Exercise 12 completed (all four dimension tables built).
- File to edit: `dbt/models/gold/fact_sales.sql`
- Verification:
  ```sql
  SELECT COUNT(*), SUM(total_amount)
  FROM gold.fact_sales;
  ```
  Row count should match `bronze.orders`. `SUM(total_amount)` is your
  total all-time revenue.

  Cross-check with a join:
  ```sql
  SELECT r.region_name, SUM(f.total_amount) AS revenue
  FROM gold.fact_sales f
  JOIN gold.dim_region r ON f.region_key = r.region_key
  GROUP BY r.region_name
  ORDER BY revenue DESC;
  ```
