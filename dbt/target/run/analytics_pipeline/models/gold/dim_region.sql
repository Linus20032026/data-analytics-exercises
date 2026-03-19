
  
    

  create  table "analytics_demo"."gold"."dim_region__dbt_tmp"
  
  
    as
  
  (
    

SELECT
    region_sk   AS region_key,
    region_id,
    region_name,
    country,
    continent
FROM "analytics_demo"."silver"."silver_regions"
  );
  