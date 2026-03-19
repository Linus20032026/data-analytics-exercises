-- Exercise 7: Staging model for clients
-- Source table : bronze.clients
-- Destination  : silver schema (view), tag: staging
--
-- Steps:
--   1. SELECT all five columns from bronze.clients.
--   2. TRIM whitespace from every text column.
--   3. Additionally LOWER() the email column.
--   4. Filter out rows where client_id IS NULL.
--
-- Columns to expose: client_id, client_name, client_type, region_id, email

{{ config(materialized='view', schema='silver', tags=['staging']) }}

SELECT
    -- your columns here
FROM bronze.clients
WHERE -- your filter here
