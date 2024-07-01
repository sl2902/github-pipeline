"""Script that downloads PyPi responses"""
import psycopg2
import psycopg2.extras
import os
import sys
import re
import pypistats
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv
from typing import Dict, List, Optional
from utils.pypi_api_requests import get_recent_endpoints
from utils.db_operations import (
                           check_pypi_apis_last_run,
                           insert_pypi_raw_endpoints,
                           insert_pypi_last_api_run)
from utils.db_connection import make_db_connection

_ = load_dotenv()

packages = [
    "pyiceberg",
    "delta-spark",
]

def process_requests(package: str, endpoint: str):
    """Process each endpoint"""
    mesg, status = [], ""
    is_inserted = False
    load_type = None
    try:
        conn = make_db_connection()
        cur = conn.cursor()
    except psycopg2.OperationalError as e:
        raise Exception(f'Could not create Postgres connection: {e}')
    
    try:
        result = check_pypi_apis_last_run(cur, package, endpoint)
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        yesterday = today - timedelta(1)
        if result:
            load_type, end_date = result
            # had to do this conversion as the return type form postgre is of class datetime.date
            # but format is %Y-%m-%d and not datetime()
            end_date = datetime.strptime(datetime.strftime(end_date, "%Y-%m-%d"), "%Y-%m-%d")
            if load_type == "history" and (today - end_date).days <= 180:
                print(f"History already downloaded for package {package}. Data is only {(today - end_date).days} days old.", end="")
                print(" Should be over 180 days")
                status = "Success"
            elif load_type == "daily" and end_date == yesterday:
                print("API has run for most recent response")
                status = "Success"
            else:
                print(f"Fetching response for package {package} and endpoint {endpoint}")
                mesg, status = get_recent_endpoints(package, endpoint)
                # format mesg to match format for history load
                if isinstance(mesg.get("data"), dict):
                    mesg["data"]["date"] = datetime.strftime(yesterday, format="%Y-%m-%d")
                    mesg["data"]["category"] = "without_mirrors"
                    mesg["data"]["downloads"] = mesg["data"].get("last_day")
                    del mesg["data"]["last_day"]
        else:
            if load_type == "history":
                print(f"Fetching response for last 180 days for package {package} and endpoint {endpoint}")
            else:
                print(f"Fetching recent response for package {package} and endpoint {endpoint}")
            mesg, status = get_recent_endpoints(package, endpoint)
            if isinstance(mesg.get("data"), dict):
                mesg["data"]["date"] = datetime.strftime(yesterday, format="%Y-%m-%d")
                mesg["data"]["category"] = "without_mirrors"
                mesg["data"]["downloads"] = mesg["data"].get("last_day")
                del mesg["data"]["last_day"]

        try:
            if len(mesg) == 0 and status == "Success":
                print(f"Possibly no responses for package {package} and endpoint {endpoint}")
            elif len(mesg) == 0 and status == "Failure":
                print(f"Parsing JSON failed for package {package} and endpoint {endpoint}")
            else:
                insert_pypi_raw_endpoints(cur, package, endpoint, mesg.get("data"))
                if isinstance(mesg.get("data"), dict):
                    print(f"Inserted 1 record for package {package} and endpoint {endpoint}")
                else:
                    print(f"Inserted {len(mesg.get('data'))} records for {package} and endpoint {endpoint}")
                is_inserted = True
        except Exception as e:
            print(f'Bulk insert failed for package {package} and endpoint {endpoint}: {e}')
            raise e

        if is_inserted:
            end_date = today - timedelta(1)
            start_date = end_date - timedelta(180)
            try:
                if isinstance(mesg.get("data"), list):
                    insert_pypi_last_api_run(cur, package, endpoint, start_date, end_date, "history", "success")
                else:
                    insert_pypi_last_api_run(cur, package, endpoint, end_date, end_date, "daily", "success")
            except Exception as e:
                print(f"Insert into tracking table failed for package {package} and endpoint {endpoint}: {e}")
                raise e
            is_inserted = False
            conn.commit()
    
    except Exception as e:
        conn.rollback()
        print(f"Rollback most recent transactions for package {package} and endpoint {endpoint}")
        print(f"Pipeline failed with error: {e}")

    cur.close()
    conn.close()

def generate_concurrent_requests(endpoint: str):
    """Process multiple requests"""
    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = [executor.submit(process_requests, package, endpoint) 
                   for package in packages]
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Processing failed with error: {e}")

if __name__ == "__main__":
    generate_concurrent_requests("overall")