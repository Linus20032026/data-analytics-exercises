
  
    

  create  table "analytics_demo"."gold"."fact_sales__dbt_tmp"
  
  
    as
  
  (
    

SELECT
    order_sk                                        AS sale_key,
    date_key,
    client_sk                                       AS client_key,
    product_sk                                      AS product_key,
    region_sk                                       AS region_key,
    quantity,
    unit_price,
    discount_pct,
    total_amount
FROM "analytics_demo"."silver"."silver_orders"
  );
  