# Exercise 10 — Silver models: clients and products

## Task
Write the SELECT statements for two silver models.

**`dbt/models/silver/silver_products.sql`**
1. Reference `{{ ref('stg_products') }}`.
2. Generate `product_sk` from `product_id` using the MD5 pattern.
3. Pass through: `product_id`, `product_name`, `category`, `subcategory`, `list_price`.
4. Add `CURRENT_TIMESTAMP AS loaded_at`.

**`dbt/models/silver/silver_clients.sql`** (requires a JOIN)
1. Reference `{{ ref('stg_clients') }}` (alias `c`) and
   LEFT JOIN `{{ ref('silver_regions') }}` (alias `r`) on `c.region_id = r.region_id`.
2. Generate `client_sk` from `c.client_id`.
3. Pass through: `client_id`, `client_name`, `client_type`, `email`, `region_id`.
4. Include `r.region_sk` (foreign key to `silver_regions`).
5. Add `CURRENT_TIMESTAMP AS loaded_at`.

## Goal
See how the surrogate key pattern scales to related entities. `silver_clients`
introduces a cross-model join — pulling `region_sk` from the already-built
`silver_regions` so the foreign key relationship is encoded in the silver layer
before data reaches the gold layer.

## What is needed
- Exercise 9 completed (`silver_regions` built and verified).
- Files to edit:
  - `dbt/models/silver/silver_products.sql`
  - `dbt/models/silver/silver_clients.sql`
- Verification:
  ```sql
  SELECT client_sk, client_name, region_sk
  FROM silver.silver_clients LIMIT 5;
  -- region_sk should be non-null (matches a region_sk in silver_regions)

  SELECT product_sk, product_name
  FROM silver.silver_products LIMIT 5;
  ```
