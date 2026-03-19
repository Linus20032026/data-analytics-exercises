-- Exercise 8: Staging model for products
-- Source table : bronze.products
-- Destination  : silver schema (view), tag: staging
--
-- Steps:
--   1. SELECT all five columns from bronze.products.
--   2. TRIM whitespace from all text columns.
--   3. Cast list_price to NUMERIC.
--   4. Filter out rows where product_id IS NULL.
--
-- Columns to expose: product_id, product_name, category, subcategory, list_price

{{ config(materialized='view', schema='silver', tags=['staging']) }}

SELECT
    -- your columns here
FROM bronze.products
WHERE -- your filter here
