FROM python:3.11-slim

RUN pip install --no-cache-dir dbt-postgres==1.7.17 flask==3.0.3

WORKDIR /dbt

CMD ["python", "server.py"]
