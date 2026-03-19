# Data Analytics Exercises
## From CSV to Superset Dashboard — 15 Exercises

> **Goal:** Build a fully working analytics data warehouse step by step.
> You start with four CSV files and finish with live Superset charts.

---

## Stack overview

```
data/raw/*.csv
      ↓  Airflow (ETL orchestration)
  [bronze schema]  Raw TEXT tables in PostgreSQL
      ↓  dbt staging models
  [silver schema]  Typed + surrogate-keyed tables
      ↓  dbt gold models
  [gold schema]    Star schema (dims + fact)
      ↓
  Apache Superset  Dashboards & SQL Lab
```

| Service    | URL                   | Login         |
|------------|-----------------------|---------------|
| Airflow    | http://localhost:8088 | admin / admin |
| Superset   | http://localhost:8089 | admin / admin |
| PostgreSQL | localhost:5432        | admin / admin |
| dbt HTTP   | http://localhost:8087 | —             |

### Quick start

```bash
docker-compose up -d
# Wait ~60 s for Airflow to init, then open http://localhost:8088
```

---

## Block A — Environment Setup (Exercises 1–2)

### Exercise 1 — Start the stack

```bash
docker-compose up -d
```

1. Open Docker Desktop and confirm **four** containers are running:
   `postgres`, `dbt`, `airflow`, `superset`.
2. Wait about 60 seconds for Airflow to finish its `db init`.
3. Open http://localhost:8088 and log in with `admin / admin`.
4. Navigate to **DAGs** and confirm `etl_full_pipeline` is listed
   (it will be in a *failed* state — that is expected at this stage).

### Exercise 2 — Explore the raw data

The folder `data/raw/` contains four CSV files:

| File           | Key columns                                                          |
|----------------|----------------------------------------------------------------------|
| `regions.csv`  | region_id, region_name, country, continent                           |
| `clients.csv`  | client_id, client_name, client_type, region_id, email                |
| `products.csv` | product_id, product_name, category, subcategory, list_price          |
| `orders.csv`   | order_id, order_date, client_id, product_id, quantity, unit_price, discount_pct |

Open each file and answer:

1. What is the data type of every column? Which ones need casting?
2. Are there any obviously dirty values (extra spaces, mixed case)?
3. What joins would you need to produce a single flat sales table?

---

## Block B — Bronze Layer: Load Raw CSV into PostgreSQL (Exercises 3–5)

> File to edit: `dags/etl_pipeline.py`

All bronze tasks call the helper `_load_csv(table, csv_path, columns)`.
Implement the helper first, then wire up each task.

### Exercise 3 — Implement `_load_csv()` and load regions

Implement `_load_csv()` in `dags/etl_pipeline.py`:

```
Steps (see docstring in the file):
  1. Use glob.glob(csv_path) to find matching files.
     → Raise FileNotFoundError if the list is empty.
  2. Open a psycopg2 connection using the DB_CONN dict.
  3. CREATE TABLE IF NOT EXISTS bronze.<table>
     with every column declared as TEXT.
  4. TRUNCATE the table (so re-runs are idempotent).
  5. For each file: read with csv.DictReader, build a list of
     value tuples, INSERT with cursor.executemany().
  6. conn.commit() and close the connection.
```

Then implement `load_regions()`:
```python
def load_regions():
    _load_csv(
        table    = "regions",
        csv_path = "/opt/data/raw/regions.csv",
        columns  = ["region_id", "region_name", "country", "continent"],
    )
```

**Verify:** In Airflow, trigger the DAG and check that only the
`load_raw.load_regions` task turns green. Then:
```sql
SELECT * FROM bronze.regions LIMIT 5;
```

### Exercise 4 — Load clients and products

Implement `load_clients()` and `load_products()` following the same pattern.

```
Clients columns : client_id, client_name, client_type, region_id, email
Products columns: product_id, product_name, category, subcategory, list_price
```

**Verify:**
```sql
SELECT COUNT(*) FROM bronze.clients;
SELECT COUNT(*) FROM bronze.products;
```

### Exercise 5 — Load orders

Implement `load_orders()`.

```
Orders columns: order_id, order_date, client_id, product_id,
                quantity, unit_price, discount_pct
```

**Verify:** All four `load_raw.*` tasks turn green.
```sql
SELECT MIN(order_date), MAX(order_date), COUNT(*) FROM bronze.orders;
```

---

## Block C — Staging Layer: Clean Data with dbt (Exercises 6–8)

> Files to edit: `dbt/models/staging/stg_*.sql`
> and `dags/etl_pipeline.py` (implement `_call_dbt`)

### Exercise 6 — Implement `_call_dbt()` and trigger staging

Implement `_call_dbt(endpoint)` in `dags/etl_pipeline.py`:

```
Steps (see docstring):
  1. POST to f"{DBT_BASE}/{endpoint}" with timeout=300.
  2. Parse the JSON response body.
  3. Print result["output"] so logs are visible in Airflow.
  4. If result["returncode"] != 0, raise an Exception.
```

Then implement `run_dbt_staging()`:
```python
def run_dbt_staging():
    _call_dbt("run/staging")
```

**Test the dbt endpoint directly:**
```bash
curl -X POST http://localhost:8087/run/staging
```

### Exercise 7 — Write staging models for regions and clients

Open `dbt/models/staging/stg_regions.sql` and
`dbt/models/staging/stg_clients.sql`.

Each staging model should:
- Read from the corresponding `bronze.*` table.
- `TRIM()` all text columns.
- For clients, also `LOWER()` the email.
- Filter out rows where the primary ID column is NULL.

```sql
SELECT * FROM silver.stg_regions LIMIT 5;
SELECT * FROM silver.stg_clients LIMIT 5;
```

### Exercise 8 — Write staging models for products and orders

Open `dbt/models/staging/stg_products.sql` and
`dbt/models/staging/stg_orders.sql`.

For products and orders also **cast** columns:
- `list_price::NUMERIC`
- `order_date::DATE`
- `quantity::INTEGER`
- `unit_price::NUMERIC`, `discount_pct::NUMERIC`

**Verify:**
```sql
SELECT pg_typeof(list_price) FROM silver.stg_products LIMIT 1;
SELECT pg_typeof(order_date), pg_typeof(quantity) FROM silver.stg_orders LIMIT 1;
```

---

## Block D — Silver Layer: Surrogate Keys with dbt (Exercises 9–11)

> Files to edit: `dbt/models/silver/silver_*.sql`

The silver layer adds **integer surrogate keys** using this deterministic
MD5 pattern (memorise it — you'll use it in every silver model):
```sql
ABS(('x' || MD5(<natural_key>))::BIT(32)::INT)  AS <entity>_sk
```

### Exercise 9 — silver_regions

Open `dbt/models/silver/silver_regions.sql`.

Add a `region_sk` using the surrogate key pattern on `region_id`.
Pass through all columns from `{{ ref('stg_regions') }}`.
Add `CURRENT_TIMESTAMP AS loaded_at`.

```sql
SELECT region_sk, region_id, region_name FROM silver.silver_regions LIMIT 5;
```

### Exercise 10 — silver_clients and silver_products

**silver_products** — same pattern as silver_regions, keyed on `product_id`.

**silver_clients** — needs a JOIN:
- Generate `client_sk` from `client_id`.
- LEFT JOIN `{{ ref('silver_regions') }}` on `region_id` to bring in `region_sk`.

```sql
SELECT client_sk, client_name, region_sk FROM silver.silver_clients LIMIT 5;
```

### Exercise 11 — silver_orders (the most complex silver model)

silver_orders joins three upstream models and adds computed fields:

1. Generate `order_sk` from `order_id`.
2. Add `date_key` as `TO_CHAR(order_date, 'YYYYMMDD')::INTEGER`.
3. LEFT JOIN `silver_clients` (for `client_sk`, `region_sk`) and
   `silver_products` (for `product_sk`).
4. Compute `total_amount`:
   ```sql
   ROUND(quantity * unit_price * (1 - discount_pct), 2)
   ```
5. Add `loaded_at`.

```sql
SELECT order_sk, date_key, client_sk, product_sk, total_amount
FROM silver.silver_orders LIMIT 5;
```

---

## Block E — Gold Layer + Airflow + Superset (Exercises 12–15)

### Exercise 12 — Write the four dimension tables

Open each file in `dbt/models/gold/` and implement the four dimensions.

**dim_region** — rename `region_sk → region_key`, pass through other columns.

**dim_client** — rename `client_sk → client_key`, `region_sk → region_key`, pass through client columns.

**dim_product** — rename `product_sk → product_key`, pass through product columns.

**dim_date** — derive calendar attributes from distinct order dates in `stg_orders`.
Required columns:
```
date_key (YYYYMMDD integer), full_date, day, month, month_name,
quarter, year, day_name, day_of_week, day_of_year, is_weekend
```

```sql
SELECT * FROM gold.dim_date ORDER BY full_date LIMIT 5;
```

### Exercise 13 — Write the fact table

Open `dbt/models/gold/fact_sales.sql`.

Thin projection of `silver_orders`:
- Rename `order_sk → sale_key`.
- Pass through `date_key`.
- Rename `client_sk → client_key`, `product_sk → product_key`, `region_sk → region_key`.
- Pass through measures: `quantity`, `unit_price`, `discount_pct`, `total_amount`.

```sql
SELECT COUNT(*), SUM(total_amount) FROM gold.fact_sales;
```

### Exercise 14 — Run the full Airflow pipeline end-to-end

Implement `run_dbt_silver()` and `run_dbt_gold()` in `dags/etl_pipeline.py`
(same pattern as `run_dbt_staging` — different endpoint strings).

Trigger the full DAG in Airflow and wait for all three task groups to turn green:

```
load_raw ✓  →  silver ✓  →  gold ✓
```

### Exercise 15 — Explore the dashboard in Superset

Once Exercise 14 is complete, Superset auto-provisions the dashboard.

1. Open http://localhost:8089 (admin / admin).
2. Navigate to **Dashboards → Sales Analytics Dashboard**.
3. You should see five charts:
   - Total Revenue (KPI big number)
   - Monthly Revenue Trend (line chart)
   - Revenue by Region (bar chart)
   - Revenue by Category (pie chart)
   - Top 10 Clients (table)

**Optional explorations:**
- Open **SQL Lab** and write a query that joins `gold.fact_sales` with
  all four dimension tables to produce a flat row per sale.
- Add a new chart: "Revenue by Continent" on the `sales_analytics` dataset.
- In Airflow, trigger the DAG again — it is idempotent and safe to re-run.

---

## Troubleshooting

| Symptom | What to check |
|---------|---------------|
| Airflow task stuck in *queued* | DAG may be paused — click the toggle next to the DAG name |
| `FileNotFoundError` in load task | CSV lives at `/opt/data/raw/` inside the container |
| dbt returns `returncode: 1` | Run `docker-compose logs dbt` for the SQL error |
| Superset "dataset not found" | Run the ETL pipeline first; Superset retries every 60 s |
| Port conflict on startup | Another service is using 8087/8088/8089/5432 |

## Solutions

Working solutions for all files are in `solutions/`:

```
solutions/
  dags/etl_pipeline.py
  dbt/models/staging/stg_*.sql
  dbt/models/silver/silver_*.sql
  dbt/models/gold/dim_*.sql
  dbt/models/gold/fact_sales.sql
```
## 🙋‍♂️ Get Involved

If you encounter any issues or have questions:
- 🐛 [Report bugs](https://github.com/markusbegerow/data-analytics-exercises/issues)
- 💡 [Request features](https://github.com/markusbegerow/data-analytics-exercises/issues)
- ⭐ Star the repo if you find it useful!

## ☕ Support the Project

If you like this project, support further development with a repost or coffee:

<a href="https://www.linkedin.com/sharing/share-offsite/?url=https://github.com/MarkusBegerow/data-analytics-exercises" target="_blank"> <img src="https://img.shields.io/badge/💼-Share%20on%20LinkedIn-blue" /> </a>

[![Buy Me a Coffee](https://img.shields.io/badge/☕-Buy%20me%20a%20coffee-yellow)](https://paypal.me/MarkusBegerow?country.x=DE&locale.x=de_DE)

## 📬 Contact

- 🧑‍💻 [Markus Begerow](https://linkedin.com/in/markusbegerow)
- 💾 [GitHub](https://github.com/markusbegerow)
- ✉️ [Twitter](https://x.com/markusbegerow)
