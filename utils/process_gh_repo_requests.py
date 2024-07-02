"""Script that interacts with api_requests and db_operations"""
import psycopg2
import psycopg2.extras
import os
import sys
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv
from typing import Dict, List, Optional
from utils.api_requests import get_recent_endpoints
from utils.db_operations import (get_last_page_and_next_page,
                           check_apis_last_run,
                           insert_raw_endpoints,
                           insert_last_api_run)
from utils.db_connection import make_db_connection

_ = load_dotenv()

base_url = "https://api.github.com/repos"
# headers = {
#     'Authorization': f'token {os.getenv("GITHUB_PAT")}',
#     'Content-Type': 'application/json; charset=utf-8'
# }
# params = {'per_page': 100}
# owner = "trinodb"
# repo = "trino"
# endpoint = "issues"
repositories = [
    ("iceberg", "apache"),
    ("delta", "delta-io"),
    ("hudi", "apache")
]


def process_requests(repo: str, owner: str, endpoint: str):
    """Process each endpoint"""
    try:
        conn = make_db_connection()
        cur = conn.cursor()
    except psycopg2.OperationalError as e:
        raise Exception(f'Could not create Postgres connection: {e}')

    url = f"{base_url}/{owner}/{repo}/{endpoint}" if endpoint != "/" else f"{base_url}/{owner}/{repo}"
    # i = 0
    latest_next_url = None
    latest_next_page, latest_last_page = 1, 0
    while True:
        try:
            result = check_apis_last_run(cur, owner, repo, endpoint)
            if result:
                latest_next_url, latest_next_page, latest_last_page = result
                print(f"Fetching response from {latest_next_url}")
                response, mesg, status = get_recent_endpoints(latest_next_url, endpoint)
            else:
                print(f"Fetching response from the beginning for {owner}/{repo} endpoint {endpoint}")
                response, mesg, status = get_recent_endpoints(url, endpoint)
        
            ratelimit_remaining = int(response.headers["X-RateLimit-Remaining"])
            print(f"Fetching links for {owner}/{repo} endpoint {endpoint}")
            resp = get_link_url_and_pages(response.links)
            # print(resp)
            
            try:
                if len(mesg) == 0 and status == "Success":
                    print(f"Possibly no responses for new {endpoint}")
                elif len(mesg) == 0 and status == "Failure":
                    print(f"Parsing JSON failed")
                else:
                    insert_raw_endpoints(cur, owner, repo, endpoint, mesg)
                    if isinstance(mesg, dict):
                        print(f"Inserted 1 record for {owner}/{repo} endpoint {endpoint}")
                    else:
                        print(f"Inserted {len(mesg)} records for {owner}/{repo} endpoint {endpoint}")
            except Exception as e:
                print(f'Bulk insert failed for {owner}/{repo} endpoint {endpoint} failed: {e}')
                raise

            if ratelimit_remaining <= 0:
                print(f"Ratelimit has been exhausted for {owner}/{repo} endpoint {endpoint}")
                insert_last_api_run(cur, owner, repo, endpoint, url, resp["next_url"], 
                    resp["next_page"], resp["last_page"], status)
                conn.commit()
                break
            # some endpoints have no links. Example - languages
            elif len(response.links) > 0:
                # check to ensure the latest next_url is not gt than last_page
                if latest_last_page > 0:
                    print(f"{owner}/{repo} - lastest_next_page, {latest_next_page}, latest_last_page, {latest_last_page}")
                    if latest_next_page > latest_last_page:
                        print(f"No new responses from {owner}/{repo} endpoint {endpoint} since the last hour")
                        break
                if "next" in response.links:
                    insert_last_api_run(cur, owner, repo, endpoint, url, resp["next_url"], 
                                        resp["next_page"], resp["last_page"], status)
                    conn.commit()
                else:
                    # scenario when you reach the last page
                    print(f"You have reached the maximum number of pages provided by {owner}/{repo} endpoint {endpoint}. Update url tracker")
                    # sometimes throws error that \\ not supported inside {}
                    resp["next_url"] = re.sub(r'(.*?)(?<!_)page=\d+', "\\1page={}".format(resp["next_page"]), resp["prev_url"])
                    insert_last_api_run(cur, owner, repo, endpoint, url, resp["next_url"],
                                        resp["next_page"], resp["last_page"], status)
                    conn.commit()
                    break
            else:
                print(f"The {owner}/{repo} endpoint {endpoint} has no links")
                if status == "Success":
                    conn.commit()
                break

            # if i > 1:
            #     break
            # i += 1

        except Exception as e:
            conn.rollback()
            print(f"Rollback most recent transactions for {owner}/{repo} endpoint {endpoint}")
            print(f"Pipeline failed with error: {e}")
            break

    cur.close()
    conn.close()

def get_link_url_and_pages(links: Dict) -> Dict:
    """Fetch the next_page, next_url, last_page
    last_url, prev_page and prev_url from links
    """
    # next_url, last_url = None, None
    # next_page, last_page = 2, 99999999
    resp = {}
    if len(links) > 0:
        if "next" in links:
            resp["next_url"] = links.get('next').get('url') if links.get('next') else None
            resp["last_url"] = links.get('last').get('url') if links.get('last') else None
            resp["next_page"] = int(re.search(r'(?<=&page=)\d+', resp["next_url"])[0])
            resp["last_page"] = int(re.search(r'(?<=&page=)\d+', resp["last_url"])[0])

        else:
            # scenario when you reach the last page
            resp["prev_url"] = links.get('prev').get('url') if links.get('prev') else None
            resp["prev_page"] = int(re.search(r'(?<=&page=)\d+', resp["prev_url"])[0])
            resp["next_page"] = resp["prev_page"] + 2
            resp["last_page"] = resp["prev_page"] + 1

    return resp

def generate_concurrent_requests(endpoint: str):
    """Process multiple requests"""
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(process_requests, repo, owner, endpoint) 
                   for (repo, owner) in repositories]
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Processing failed with error: {e}")


# if __name__ == "__main__":
#     generate_concurrent_requests(endpoint)

    