"""Script queries the relevant endpoint from the upstream db"""
import psycopg2
import psycopg2.extras
import logging
from typing import Any, Optional, Dict, List, Tuple, Union
from datetime import datetime, timedelta
from utils.db_connection import make_db_connection
from kafka_producer.pg_upstream_queries import *

logger = logging.getLogger("airflow.task")

try:
    conn = make_db_connection()
    cur = conn.cursor()
except psycopg2.OperationalError as e:
    raise Exception(f'Could not create Postgres connection: {e}')

def fetch_query(endpoint: str) -> str:
    """Fetch raw query string"""
    if endpoint in raw_qry_str:
        return  raw_qry_str.get(endpoint)

def get_stg_table_decription():
    """Get column names from gh_staging_raw_endpoints"""
    pass


def query_upstream_db(
        endpoint: str
) -> List[Dict[str, str]]: 
    """Fetch events for an endpoint"""
    qry = fetch_query(endpoint)
    if qry is not None:
        cur.execute(qry)
        cols = [desc[0] for desc in cur.description]
    else:
        raise KeyError(f"Endpoint {endpoint} is not present")
    return [dict(zip(cols, row)) for row in cur.fetchall()]


