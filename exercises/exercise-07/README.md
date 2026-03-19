# Exercise 7 — Staging models: regions and clients

## Task
Write the SELECT statements in two dbt staging models.

**`dbt/models/staging/stg_regions.sql`**
- Read from `bronze.regions`.
- `TRIM()` every text column.
- Filter: `WHERE region_id IS NOT NULL`.
- Expose columns: `region_id`, `region_name`, `country`, `continent`.

**`dbt/models/staging/stg_clients.sql`**
- Read from `bronze.clients`.
- `TRIM()` every text column.
- Additionally apply `LOWER()` to `email`.
- Filter: `WHERE client_id IS NOT NULL`.
- Expose columns: `client_id`, `client_name`, `client_type`, `region_id`, `email`.

After writing both files, trigger the dbt staging run:
```bash
curl -X POST http://localhost:8087/run/staging
```

## Goal
Learn the role of the staging layer: light cleaning only (trim, lowercase,
null-filter) with no type casting and no joins. Staging views are the
single source of truth for all downstream models.

## What is needed
- Exercise 6 completed (`_call_dbt()` implemented).
- Files to edit:
  - `dbt/models/staging/stg_regions.sql`
  - `dbt/models/staging/stg_clients.sql`
- The `{{ config(...) }}` block at the top of each file is already provided —
  do not remove it; just fill in the SELECT statement.
- Verification queries:
  ```sql
  SELECT * FROM silver.stg_regions LIMIT 5;
  SELECT * FROM silver.stg_clients LIMIT 5;
  ```
