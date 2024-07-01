'''Script to execute DB statements'''
import psycopg2
import psycopg2.extras
import os
import time
import json
import re
import hashlib
import logging
# from dotenv import load_dotenv
from typing import Optional, Dict, List, Tuple, Union
from datetime import datetime, timedelta
from utils.db_connection import make_db_connection

logger = logging.getLogger("airflow.task")


# _ = load_dotenv()

def get_last_page_and_next_page(
        cur: psycopg2.extensions.cursor, 
        owner: str,
        repo: str,
        endpoint: str
) -> bool:
    """Fetch the most recent next_page"""
    qry = """
        SELECT
            next_page
        FROM
            gh_track_raw_endpoints
        WHERE
            owner = %s
        AND
            repo = %s
        AND
            endpoint = %s
        ORDER BY
            last_updated_at DESC
        LIMIT 1;
        """
    params = (owner, repo, endpoint)
    cur.execute(qry, params)
    # print(cur.mogrify(qry, params).decode('utf8'))
    row = cur.fetchone()
    return row if row else None

def check_apis_last_run(
        cur: psycopg2.extensions.cursor, 
        owner: str,
        repo: str,
        endpoint: str
) -> Optional[str]:
    """Return the latest next_url and next_page for an endpoint if exists"""
    qry = """
        SELECT
            next_url,
            next_page,
            last_page
        FROM
            gh_track_raw_endpoints
        WHERE
            owner = %s
        AND
            repo = %s
        AND
            endpoint = %s
        ORDER BY
            last_updated_at DESC
        LIMIT 1;
        """
    params = (owner, repo, endpoint)
    cur.execute(qry, params)
    # print(cur.mogrify(qry, params).decode('utf8'))
    row = cur.fetchone()
    return row if row else None

def insert_raw_endpoints(
        cur: psycopg2.extensions.cursor,
        owner: str,
        repo: str,
        endpoint: str,
        resp: Union[List[Dict], Dict],
):
    """Insert raw endpoints responses from the GitHub API"""
    qry = """
        INSERT INTO gh_staging_raw_endpoints(owner, repo, endpoint, response, response_md5)
        VALUES %s
        ON CONFLICT (endpoint, response_md5) DO NOTHING;
    """
    try:
        if isinstance(resp, dict):
            params = [(
                owner, 
                repo, 
                endpoint, 
                # to avoid any UTF8 encoding issue
                json.dumps(resp, ensure_ascii=False).replace(r"\u0000", ""), 
                hashlib.md5(json.dumps(resp, ensure_ascii=False).encode()).hexdigest()
            )]
        else:
            params = []
            for record in resp:
                response_json = json.dumps(record, ensure_ascii=False).replace(r"\u0000", "")
                response_md5 = hashlib.md5(response_json.encode()).hexdigest()
                params.append((owner, repo, endpoint, response_json, response_md5))
        # print(cur.mogrify(qry, params).decode('utf8'))
        psycopg2.extras.execute_values(cur, qry, params)
    except psycopg2.Error as e:
        print(f"Database error: {e.pgcode} - {e.pgerror}")
        print(f"Details: {e.diag.message_detail}")
        print(f"Context: {e.diag.context}")
    except Exception as e:
        return

def insert_last_api_run(
        cur: psycopg2.extensions.cursor,
        owner: str,
        repo: str,
        endpoint: str, 
        url: str,
        next_url: str,
        next_page: int,
        last_page: int,
        status: str
):
    """Capture the last run endpoint API to keep track of where to start from
    next time
    """
    qry = """INSERT INTO gh_track_raw_endpoints (owner, repo, endpoint, url, next_url, next_page, last_page, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
    cur.execute(qry, (owner, repo, endpoint, url, next_url, next_page, last_page, status))

def check_pypi_apis_last_run(
        cur: psycopg2.extensions.cursor, 
        package,
        endpoint: str
) -> Optional[str]:
    """Return the latest run for an endpoint if exists"""
    qry = """
        SELECT
           load_type,
           end_date
        FROM
            pypi_track_raw_endpoints
        WHERE
            endpoint = %s
        AND
            package = %s
        AND
            status = 'success'
        ORDER BY
            last_updated_at DESC
        LIMIT 1;
        """
    params = (endpoint, package)
    cur.execute(qry, params)
    # print(cur.mogrify(qry, params).decode('utf8'))
    row = cur.fetchone()
    return row if row else None

def insert_pypi_raw_endpoints(
        cur: psycopg2.extensions.cursor,
        package: str,
        endpoint: str,
        resp: Union[List[Dict], Dict]
):
    """Insert raw endpoints responses from the Pypi API"""
    qry = """
        INSERT INTO pypi_staging_raw_endpoints(package, endpoint, response, response_md5)
        VALUES %s
        ON CONFLICT (endpoint, response_md5) DO NOTHING;
    """
    try:
        if isinstance(resp, dict):
            params = [(
                package,
                endpoint, 
                # to avoid any UTF8 encoding issue
                json.dumps(resp, ensure_ascii=False).replace(r"\u0000", ""), 
                hashlib.md5(json.dumps(resp, ensure_ascii=False).encode()).hexdigest()
            )]
        else:
            params = []
            for record in resp:
                response_json = json.dumps(record, ensure_ascii=False).replace(r"\u0000", "")
                response_md5 = hashlib.md5(response_json.encode()).hexdigest()
                params.append((package, endpoint, response_json, response_md5))
        # print(cur.mogrify(qry, params).decode('utf8'))
        psycopg2.extras.execute_values(cur, qry, params)
    except psycopg2.Error as e:
        print(f"Database error: {e.pgcode} - {e.pgerror}")
        print(f"Details: {e.diag.message_detail}")
        print(f"Context: {e.diag.context}")
    except Exception as e:
        return

def insert_pypi_last_api_run(
        cur: psycopg2.extensions.cursor,
        package: str,
        endpoint: str, 
        start_date: str,
        end_date: str,
        load_type: str,
        status: str
):
    """Capture the last run endpoint API to keep track of where to start from
    next time
    """
    qry = """INSERT INTO pypi_track_raw_endpoints (package, endpoint, start_date, end_date, load_type, status)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
    cur.execute(qry, (package, endpoint, start_date, end_date, load_type, status))
