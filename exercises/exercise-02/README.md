# Exercise 2 — Explore the raw data

## Task
Open the four CSV files in `data/raw/` (use Excel, a text editor, or
`head -5 data/raw/<file>.csv`) and answer the following questions for
each file:

1. What are the column names and their apparent data types?
2. Which columns will need type casting before analysis (e.g. TEXT → DATE, INTEGER, NUMERIC)?
3. Are there dirty values — extra whitespace, mixed-case strings, empty cells?
4. Which column acts as the natural primary key?
5. How would you join the four tables to produce a single flat sales row?

## Goal
Build a mental model of the source data before writing any code.
Understanding what needs cleaning (whitespace, casing, type casting)
and how the tables relate to each other is the foundation for every
later exercise.

## What is needed
- Exercises 1 completed (stack running).
- Files to inspect:

| File                     | Key columns                                                              |
|--------------------------|--------------------------------------------------------------------------|
| `data/raw/regions.csv`   | region_id, region_name, country, continent                               |
| `data/raw/clients.csv`   | client_id, client_name, client_type, region_id, email                    |
| `data/raw/products.csv`  | product_id, product_name, category, subcategory, list_price              |
| `data/raw/orders.csv`    | order_id, order_date, client_id, product_id, quantity, unit_price, discount_pct |

No code changes required in this exercise.
