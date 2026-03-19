
  
    

  create  table "analytics_demo"."silver"."silver_clients__dbt_tmp"
  
  
    as
  
  (
    

SELECT
    ABS(('x' || MD5(c.client_id))::BIT(32)::INT) AS client_sk,
    c.client_id,
    c.client_name,
    c.client_type,
    c.email,
    c.region_id,
    r.region_sk,
    CURRENT_TIMESTAMP                             AS loaded_at
FROM "analytics_demo"."silver"."stg_clients" c
LEFT JOIN "analytics_demo"."silver"."silver_regions" r
    ON c.region_id = r.region_id
  );
  