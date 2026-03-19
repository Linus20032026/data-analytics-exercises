
  create view "analytics_demo"."silver"."stg_regions__dbt_tmp"
    
    
  as (
    

SELECT
    TRIM(region_id)     AS region_id,
    TRIM(region_name)   AS region_name,
    TRIM(country)       AS country,
    TRIM(continent)     AS continent
FROM bronze.regions
WHERE region_id IS NOT NULL
  );