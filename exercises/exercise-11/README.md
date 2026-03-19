# Exercise 11 — Silver model: orders (three-way join + computed field)

## Task
Open `dbt/models/silver/silver_orders.sql` and write the SELECT statement.

Requirements:
1. Reference `{{ ref('stg_orders') }}` (alias `o`).
2. LEFT JOIN `{{ ref('silver_clients') }}` (alias `c`) on `o.client_id = c.client_id`.
3. LEFT JOIN `{{ ref('silver_products') }}` (alias `p`) on `o.product_id = p.product_id`.
4. Generate `order_sk` from `o.order_id` using the MD5 surrogate key pattern.
5. Add `date_key`:
   ```sql
   TO_CHAR(o.order_date, 'YYYYMMDD')::INTEGER  AS date_key
   ```
6. Pass through order columns: `order_id`, `order_date`, `client_id`, `product_id`,
   `quantity`, `unit_price`, `discount_pct`.
7. Include foreign keys from joins: `c.client_sk`, `p.product_sk`, `c.region_sk`.
8. Compute the revenue measure:
   ```sql
   ROUND(o.quantity * o.unit_price * (1 - o.discount_pct), 2)  AS total_amount
   ```
9. Add `CURRENT_TIMESTAMP AS loaded_at`.

## Goal
Build the most complex silver model: a three-way join that assembles all
surrogate keys onto the order row, and computes `total_amount` once so
every downstream query can use it without re-implementing the formula.
`date_key` (YYYYMMDD integer) is the FK that will link to `dim_date` in the gold layer.

## What is needed
- Exercise 10 completed (`silver_clients` and `silver_products` built).
- File to edit: `dbt/models/silver/silver_orders.sql`
- Verification:
  ```sql
  SELECT order_sk, date_key, client_sk, product_sk, region_sk, total_amount
  FROM silver.silver_orders
  LIMIT 5;
  ```
  All surrogate key columns should be non-null.
  `total_amount` should be `quantity * unit_price * (1 - discount_pct)` rounded to 2 dp.
