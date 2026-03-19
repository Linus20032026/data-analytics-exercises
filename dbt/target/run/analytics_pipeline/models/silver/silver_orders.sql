
  
    

  create  table "analytics_demo"."silver"."silver_orders__dbt_tmp"
  
  
    as
  
  (
    

SELECT
    ABS(('x' || MD5(o.order_id))::BIT(32)::INT) AS order_sk,
    o.order_id,
    o.order_date,
    TO_CHAR(o.order_date, 'YYYYMMDD')::INTEGER   AS date_key,
    o.client_id,
    c.client_sk,
    o.product_id,
    p.product_sk,
    c.region_sk,
    o.quantity,
    o.unit_price,
    o.discount_pct,
    ROUND(
        o.quantity * o.unit_price * (1 - o.discount_pct), 2
    )                                            AS total_amount,
    CURRENT_TIMESTAMP                            AS loaded_at
FROM "analytics_demo"."silver"."stg_orders" o
LEFT JOIN "analytics_demo"."silver"."silver_clients"  c ON o.client_id  = c.client_id
LEFT JOIN "analytics_demo"."silver"."silver_products" p ON o.product_id = p.product_id
  );
  