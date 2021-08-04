import urllib3
from urllib3.exceptions import TimeoutError
import time
import json


http = urllib3.PoolManager()


def fetch_url(url):
    while True:
        try:
            response = http.request('GET', url)
            break
        except TimeoutError:
            print('timeout retry after 10secs: {}'.format(url))
            time.sleep(10)
    if response.status != 200:
        print('Status code: {}'.format(response.status))
    return response.data


def fetch_url_to_json(url):
    while True:
        try:
            response = http.request('GET', url)
            break
        except TimeoutError:
            print('timeout retry after 10secs: {}'.format(url))
            time.sleep(10)
    if response.status != 200:
        print('Status code: {}'.format(response.status))
    return json.loads(response.data.decode('utf-8'))
