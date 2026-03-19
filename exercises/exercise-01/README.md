# Exercise 1 — Start the stack

## Task
1. Open a terminal in the `data-analytics-exercises` directory.
2. Run:
   ```bash
   docker-compose up -d
   ```
3. Wait about 60 seconds for Airflow to finish its database initialisation.
4. Open http://localhost:8088 in your browser and log in with `admin / admin`.
5. Navigate to **DAGs** and confirm the DAG `etl_full_pipeline` is listed.

## Goal
Verify that the full four-service stack starts correctly and that Airflow
is reachable. At this point the DAG is expected to be in a *failed* or
*paused* state — that is normal. The goal is simply to confirm the
infrastructure is up before you write any code.

## What is needed
- Docker Desktop installed and running.
- Run `docker-compose up -d` from the project root.
- Confirm four containers are healthy in Docker Desktop:
  `postgres`, `dbt`, `airflow`, `superset`.

| Service    | URL                   | Credentials   |
|------------|-----------------------|---------------|
| Airflow    | http://localhost:8088 | admin / admin |
| Superset   | http://localhost:8089 | admin / admin |
| PostgreSQL | localhost:5432        | admin / admin |
| dbt HTTP   | http://localhost:8087 | —             |
