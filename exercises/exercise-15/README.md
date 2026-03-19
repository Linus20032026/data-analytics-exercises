# Exercise 15 — Explore the Superset dashboard

## Task
1. Open http://localhost:8089 and log in with `admin / admin`.
2. Navigate to **Dashboards → Sales Analytics Dashboard**.
3. Verify all five charts are populated with data:
   - **Total Revenue** — KPI big number (all-time revenue)
   - **Monthly Revenue Trend** — line chart by month
   - **Revenue by Region** — bar chart
   - **Revenue by Category** — pie / donut chart
   - **Top 10 Clients** — table sorted by revenue
4. Click any chart to explore filters and drill-down options.

**Optional challenges:**
- Open **SQL Lab** and write a query that joins all five gold tables
  to produce one flat row per sale with region, client, product, and date.
- Add a new chart: "Revenue by Continent" (bar chart, group by `continent`
  from the `sales_analytics` virtual dataset).
- Trigger the Airflow DAG a second time — confirm the numbers do not
  change (the pipeline is idempotent, same CSV → same results).

## Goal
See the full data journey: the CSV files you started with in Exercise 2
are now driving live, interactive business intelligence dashboards.
Understand how the virtual dataset (`sales_analytics`) acts as a
pre-joined flat view over the star schema, making chart creation easy.

## What is needed
- Exercise 14 completed (full Airflow pipeline ran successfully).
- Superset at http://localhost:8089 (admin / admin).
- The dashboard is auto-provisioned by `init/superset_setup.py`, which
  runs in the background when the stack starts and retries every 60 s
  until the mart tables exist.
- If the dashboard is missing, check the Superset container logs:
  ```bash
  docker-compose logs superset
  ```
  Look for "Done! Dashboard at …" — if it hasn't appeared yet, wait
  a minute and refresh.

---

**Congratulations — you have built a complete data warehouse pipeline
from raw CSV files to a live analytics dashboard.**
