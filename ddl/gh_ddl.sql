
\c postgres;
DROP DATABASE IF EXISTS gh_raw_db;
CREATE DATABASE gh_raw_db;
\c gh_raw_db;
DROP TABLE IF EXISTS gh_staging_raw_endpoints;

CREATE TABLE gh_staging_raw_endpoints (
    id SERIAL PRIMARY KEY,
    owner VARCHAR(20),
    repo VARCHAR(20),
    endpoint VARCHAR(20),
    response JSONB,
    response_md5 CHAR(32),
    created_date TIMESTAMP NOT NULL DEFAULT NOW(),
    UNIQUE (endpoint, response_md5)
);

DROP TABLE IF EXISTS gh_track_raw_endpoints;

CREATE TABLE gh_track_raw_endpoints (
        id SERIAL PRIMARY KEY,
        owner VARCHAR(20),
        repo VARCHAR(20),
        endpoint VARCHAR(20),
        url TEXT,
        next_url TEXT,
        next_page INT,
        last_page INT,
        status VARCHAR(10),
        last_updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);