"""
dbt trigger server
------------------
Exposes a minimal HTTP API so Airflow (or a student) can run dbt models
without needing dbt installed locally.

  POST /run              — runs all models: dbt run
  POST /run/staging      — runs only staging models
  POST /run/silver       — runs only silver models
  POST /run/gold         — runs only gold models
  POST /test             — runs: dbt test
  GET  /health           — liveness check
"""

import subprocess
from flask import Flask, jsonify

app = Flask(__name__)
DBT_DIR = "/dbt"
DBT_FLAGS = ["--no-use-colors", "--profiles-dir", DBT_DIR, "--project-dir", DBT_DIR]


def _run(args: list[str]) -> dict:
    # Global flags like --profiles-dir must come AFTER the sub-command in dbt 1.7
    cmd = ["dbt"] + args + DBT_FLAGS
    result = subprocess.run(cmd, capture_output=True, text=True)
    output = result.stdout + result.stderr
    print(output, flush=True)
    return {"returncode": result.returncode, "output": output}


def _check(result: dict):
    return jsonify(result), (200 if result["returncode"] == 0 else 500)


@app.get("/health")
def health():
    return "ok"


@app.post("/run")
def run_all():
    return _check(_run(["run"]))


@app.post("/run/staging")
def run_staging():
    return _check(_run(["run", "--select", "tag:staging"]))


@app.post("/run/silver")
def run_silver():
    return _check(_run(["run", "--select", "tag:silver"]))


@app.post("/run/gold")
def run_gold():
    return _check(_run(["run", "--select", "tag:gold"]))


@app.post("/test")
def test():
    return _check(_run(["test"]))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8087)
