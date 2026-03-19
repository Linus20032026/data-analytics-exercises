

SELECT
    product_sk      AS product_key,
    product_id,
    product_name,
    category,
    subcategory,
    list_price
FROM "analytics_demo"."silver"."silver_products"