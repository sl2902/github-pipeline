'''Script reads Github API to fetch reponses to various endpoints'''
import requests
from requests.exceptions import HTTPError
import os
import time
import json
import re
from dotenv import load_dotenv
from typing import Optional, Dict, List, Tuple
from datetime import datetime, timedelta
from http import HTTPStatus

_ = load_dotenv()

# base_url = "https://api.github.com/repos"
headers = {
    'Authorization': f'token {os.getenv("GITHUB_PAT")}',
    'Content-Type': 'application/json; charset=utf-8'
}
params = {'per_page': 100}

retry_codes = [
    HTTPStatus.TOO_MANY_REQUESTS,
    HTTPStatus.INTERNAL_SERVER_ERROR,
    HTTPStatus.BAD_GATEWAY,
    HTTPStatus.SERVICE_UNAVAILABLE,
    HTTPStatus.GATEWAY_TIMEOUT,
]


def get_recent_endpoints(
        url: str,
        endpoint: str
) -> Tuple[requests.Response, Optional[List[Dict[str, str]]], str]:
    """Fetch endpoint related record from repo"""
    status = None
    n_retry = 3
    while url:
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            mesg = response.json() #json.loads(response.content.decode('utf8'))
            status = "Success"
        except HTTPError as e:
            # https://stackoverflow.com/questions/61463224/when-to-use-raise-for-status-vs-status-code-testing
            code = e.response.status_code
            if code == 401:
                print('Unauthorized access - possible invalid or expired token')
                raise  # Stop processing on unauthorized error
            elif code in retry_codes and n_retry > 0:
                time.sleep(5)
                n_retry -= 1
                continue
            raise
        except json.JSONDecodeError as e:
            print(f"Request couldn't be decoded: {e}")
            status = "Failure"

        url = None
    return response, mesg, status


# if __name__ == "__main__":
#     get_recent_endpoints(url, endpoint)
    



