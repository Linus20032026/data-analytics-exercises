-- Exercise 7: Staging model for regions
-- Source table : bronze.regions
-- Destination  : silver schema (view), tag: staging
--
-- Steps:
--   1. SELECT all four columns from bronze.regions.
--   2. TRIM whitespace from every text column.
--   3. Filter out rows where region_id IS NULL.
--
-- Columns to expose: region_id, region_name, country, continent

-- TODO: replace the line below with your SELECT statement
{{ config(materialized='view', schema='silver', tags=['staging']) }}

SELECT
    -- your columns here
FROM bronze.regions
WHERE -- your filter here
