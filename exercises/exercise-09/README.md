# Exercise 9 — Silver model: regions with surrogate key

## Task
Open `dbt/models/silver/silver_regions.sql` and write the SELECT statement.

Requirements:
1. Reference the staging model with `{{ ref('stg_regions') }}`.
2. Generate an integer surrogate key using this pattern:
   ```sql
   ABS(('x' || MD5(region_id))::BIT(32)::INT)  AS region_sk
   ```
3. Pass through all source columns: `region_id`, `region_name`, `country`, `continent`.
4. Add `CURRENT_TIMESTAMP AS loaded_at`.

Trigger the silver run after writing:
```bash
curl -X POST http://localhost:8087/run/silver
```

## Goal
Understand surrogate keys: deterministic integer keys derived from the
natural key using MD5. They never change for the same input, require no
sequence or auto-increment, and work across distributed systems.
`silver_regions` is the simplest example — one table, no joins.

## What is needed
- Exercise 8 completed (all four staging models working).
- File to edit: `dbt/models/silver/silver_regions.sql`
- Surrogate key pattern to memorise (used in every silver model):
  ```sql
  ABS(('x' || MD5(<natural_key>))::BIT(32)::INT)
  ```
- Verification:
  ```sql
  SELECT region_sk, region_id, region_name
  FROM silver.silver_regions LIMIT 5;
  ```
  All `region_sk` values should be non-null positive integers.
