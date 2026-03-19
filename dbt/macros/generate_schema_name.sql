-- Override dbt's default schema naming so that +schema: silver writes to "silver",
-- not "analytics_demo_silver". This keeps schema names clean for course demos.
{% macro generate_schema_name(custom_schema_name, node) -%}
    {%- if custom_schema_name is none -%}
        {{ target.schema }}
    {%- else -%}
        {{ custom_schema_name | trim }}
    {%- endif -%}
{%- endmacro %}
