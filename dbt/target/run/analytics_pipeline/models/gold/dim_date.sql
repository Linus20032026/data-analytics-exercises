
  
    

  create  table "analytics_demo"."gold"."dim_date__dbt_tmp"
  
  
    as
  
  (
    

WITH dates AS (
    SELECT DISTINCT order_date AS full_date
    FROM "analytics_demo"."silver"."stg_orders"
)
SELECT
    TO_CHAR(full_date, 'YYYYMMDD')::INTEGER     AS date_key,
    full_date,
    EXTRACT(DAY   FROM full_date)::INTEGER       AS day,
    EXTRACT(MONTH FROM full_date)::INTEGER       AS month,
    TO_CHAR(full_date, 'Month')                  AS month_name,
    EXTRACT(QUARTER FROM full_date)::INTEGER     AS quarter,
    EXTRACT(YEAR  FROM full_date)::INTEGER       AS year,
    TO_CHAR(full_date, 'Day')                    AS day_name,
    EXTRACT(DOW   FROM full_date)::INTEGER       AS day_of_week,
    EXTRACT(DOY   FROM full_date)::INTEGER       AS day_of_year,
    CASE WHEN EXTRACT(DOW FROM full_date) IN (0,6) THEN TRUE ELSE FALSE END AS is_weekend
FROM dates
ORDER BY full_date
  );
  