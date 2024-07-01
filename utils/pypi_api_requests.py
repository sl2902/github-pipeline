'''Script reads PyPi API to fetch reponses to various packages'''
import requests
from requests.exceptions import HTTPError
import os
import time
import json
import re
import pypistats
from dotenv import load_dotenv
from typing import Optional, Dict, List, Tuple
from datetime import datetime, timedelta
from http import HTTPStatus

_ = load_dotenv()


retry_codes = [
    HTTPStatus.TOO_MANY_REQUESTS,
    HTTPStatus.INTERNAL_SERVER_ERROR,
    HTTPStatus.BAD_GATEWAY,
    HTTPStatus.SERVICE_UNAVAILABLE,
    HTTPStatus.GATEWAY_TIMEOUT,
]


def get_recent_endpoints(
        package: str,
        endpoint: str
) -> Tuple[Optional[List[Dict[str, str]]], str]:
    """Fetch package related record from PyPi"""
    try:
        if endpoint == "overall":
            mesg = json.loads(pypistats.overall(package, total=True, format="json"))
        elif endpoint == "recent":
            mesg = json.loads(pypistats.recent(package, period="day", format="json"))
        else:
            print('Valid endpoint "{recent,overall,python_major,python_minor,system}". Only 1 and 2 are covered.')
            raise Exception(f'Invalid argument {endpoint} or endpoint is not covered')
        status = "Success"
    except HTTPError as e:
        # https://stackoverflow.com/questions/61463224/when-to-use-raise-for-status-vs-status-code-testing
        code = e.response.status_code
        if code == 401:
            print('Unauthorized access - possible invalid or expired token')
            raise  # Stop processing on unauthorized error
        elif code == 404:
            print(f"Client error '404 Not Found' for url 'https://pypistats.org/api/packages/{package}/{endpoint}")
        raise
    except json.JSONDecodeError as e:
        print(f"Request couldn't be decoded: {e}")
        status = "Failure"

    return mesg, status


# if __name__ == "__main__":
#     get_recent_packages(url, package)
    
