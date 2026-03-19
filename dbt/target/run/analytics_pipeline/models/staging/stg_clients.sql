
  create view "analytics_demo"."silver"."stg_clients__dbt_tmp"
    
    
  as (
    

SELECT
    TRIM(client_id)     AS client_id,
    TRIM(client_name)   AS client_name,
    TRIM(client_type)   AS client_type,
    TRIM(region_id)     AS region_id,
    LOWER(TRIM(email))  AS email
FROM bronze.clients
WHERE client_id IS NOT NULL
  );