
  create view "analytics_demo"."silver"."stg_products__dbt_tmp"
    
    
  as (
    

SELECT
    TRIM(product_id)    AS product_id,
    TRIM(product_name)  AS product_name,
    TRIM(category)      AS category,
    TRIM(subcategory)   AS subcategory,
    list_price::NUMERIC AS list_price
FROM bronze.products
WHERE product_id IS NOT NULL
  );