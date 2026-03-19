
  create view "analytics_demo"."silver"."stg_orders__dbt_tmp"
    
    
  as (
    

-- Staging: clean raw orders data from bronze
-- Source: bronze.orders (loaded from orders.csv)

SELECT
    TRIM(order_id)          AS order_id,
    order_date::DATE        AS order_date,
    TRIM(client_id)         AS client_id,
    TRIM(product_id)        AS product_id,
    quantity::INTEGER       AS quantity,
    unit_price::NUMERIC     AS unit_price,
    discount_pct::NUMERIC   AS discount_pct
FROM bronze.orders
WHERE order_id IS NOT NULL
  AND order_date IS NOT NULL
  );