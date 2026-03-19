
  
    

  create  table "analytics_demo"."silver"."silver_regions__dbt_tmp"
  
  
    as
  
  (
    

SELECT
    ABS(('x' || MD5(region_id))::BIT(32)::INT)  AS region_sk,
    region_id,
    region_name,
    country,
    continent,
    CURRENT_TIMESTAMP                            AS loaded_at
FROM "analytics_demo"."silver"."stg_regions"
  );
  