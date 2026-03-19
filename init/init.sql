-- Analytics Demo: initial schema setup
-- Runs automatically on first Postgres startup

CREATE SCHEMA IF NOT EXISTS bronze;   -- Layer 1: raw CSV data as loaded
CREATE SCHEMA IF NOT EXISTS silver;   -- Layer 2: Silver (cleansed, typed, surrogate keys)
CREATE SCHEMA IF NOT EXISTS gold;     -- Layer 3: Gold — Star Schema (dims + fact)
