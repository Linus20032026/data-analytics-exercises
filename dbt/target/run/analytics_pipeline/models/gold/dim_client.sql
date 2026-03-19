
  
    

  create  table "analytics_demo"."gold"."dim_client__dbt_tmp"
  
  
    as
  
  (
    

SELECT
    client_sk       AS client_key,
    client_id,
    client_name,
    client_type,
    email,
    region_sk       AS region_key
FROM "analytics_demo"."silver"."silver_clients"
  );
  