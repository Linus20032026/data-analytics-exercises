#!/bin/bash
# Superset startup: init DB, create admin, init roles, start server.
# Uses IdempotentSecurityManager via SUPERSET_CONFIG_PATH so the sequence
# is safe to re-run after container restarts (checkfirst=True on create_all).

set -e

superset fab create-admin \
    --username admin \
    --firstname a \
    --lastname b \
    --email admin@x.com \
    --password admin 2>/dev/null || true

superset db upgrade
superset init

# Dashboard bootstrap runs in background; superset run stays in foreground
python /opt/init/superset_setup.py &

exec superset run -p 8088 --with-threads --host=0.0.0.0
