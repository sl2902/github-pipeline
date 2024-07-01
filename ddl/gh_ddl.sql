
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
    load_date TIMESTAMP NOT NULL DEFAULT NOW(),
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

DROP TABLE IF EXISTS pypi_staging_raw_endpoints;

CREATE TABLE pypi_staging_raw_endpoints (
    id SERIAL PRIMARY KEY,
    package VARCHAR(50),
    endpoint VARCHAR(30),
    response JSONB,
    response_md5 CHAR(32),
    load_date TIMESTAMP NOT NULL DEFAULT NOW(),
    UNIQUE (endpoint, response_md5)
);

DROP TABLE IF EXISTS pypi_track_raw_endpoints;

CREATE TABLE pypi_track_raw_endpoints (
        id SERIAL PRIMARY KEY,
        package VARCHAR(50),
        endpoint VARCHAR(20),
        start_date DATE,
        end_date DATE,
        load_type VARCHAR(10),
        status VARCHAR(10),
        last_updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);