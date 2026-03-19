

SELECT
    ABS(('x' || MD5(product_id))::BIT(32)::INT) AS product_sk,
    product_id,
    product_name,
    category,
    subcategory,
    list_price,
    CURRENT_TIMESTAMP                            AS loaded_at
FROM "analytics_demo"."silver"."stg_products"