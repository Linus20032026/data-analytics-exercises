# Exercise 12 — Gold layer: four dimension tables

## Task
Write the SELECT statements for the four dimension tables in `dbt/models/gold/`.

**`dim_region.sql`** — source: `{{ ref('silver_regions') }}`
- Rename `region_sk → region_key`.
- Pass through: `region_id`, `region_name`, `country`, `continent`.

**`dim_client.sql`** — source: `{{ ref('silver_clients') }}`
- Rename `client_sk → client_key`, `region_sk → region_key`.
- Pass through: `client_id`, `client_name`, `client_type`, `email`.

**`dim_product.sql`** — source: `{{ ref('silver_products') }}`
- Rename `product_sk → product_key`.
- Pass through: `product_id`, `product_name`, `category`, `subcategory`, `list_price`.

**`dim_date.sql`** — source: `{{ ref('stg_orders') }}` (derive from distinct dates)
- Build a CTE `dates` with `SELECT DISTINCT order_date AS full_date`.
- From the CTE, derive all calendar attributes:

  | Column        | Expression                                                            |
  |---------------|-----------------------------------------------------------------------|
  | `date_key`    | `TO_CHAR(full_date, 'YYYYMMDD')::INTEGER`  ← PK, used in fact table  |
  | `full_date`   | the DATE itself                                                       |
  | `day`         | `EXTRACT(DAY FROM full_date)::INTEGER`                                |
  | `month`       | `EXTRACT(MONTH FROM full_date)::INTEGER`                              |
  | `month_name`  | `TO_CHAR(full_date, 'Month')`                                         |
  | `quarter`     | `EXTRACT(QUARTER FROM full_date)::INTEGER`                            |
  | `year`        | `EXTRACT(YEAR FROM full_date)::INTEGER`                               |
  | `day_name`    | `TO_CHAR(full_date, 'Day')`                                           |
  | `day_of_week` | `EXTRACT(DOW FROM full_date)::INTEGER`                                |
  | `day_of_year` | `EXTRACT(DOY FROM full_date)::INTEGER`                                |
  | `is_weekend`  | `CASE WHEN EXTRACT(DOW FROM full_date) IN (0,6) THEN TRUE ELSE FALSE END` |

- `ORDER BY full_date`.

Trigger the gold run after writing all four files:
```bash
curl -X POST http://localhost:8087/run/gold
```

## Goal
Build the dimension side of the star schema. Each dimension table renames
the surrogate key to a `*_key` name (the convention used by Superset and
the fact table joins). `dim_date` is the most interesting: it is generated
entirely from order data — no external calendar source needed.

## What is needed
- Exercise 11 completed (entire silver layer built).
- Files to edit:
  - `dbt/models/gold/dim_region.sql`
  - `dbt/models/gold/dim_client.sql`
  - `dbt/models/gold/dim_product.sql`
  - `dbt/models/gold/dim_date.sql`
- Verification:
  ```sql
  SELECT * FROM gold.dim_date ORDER BY full_date LIMIT 5;
  SELECT COUNT(*) FROM gold.dim_region;
  SELECT COUNT(*) FROM gold.dim_client;
  SELECT COUNT(*) FROM gold.dim_product;
  ```
