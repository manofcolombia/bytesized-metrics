import requests
import json
import time
import argparse
import logging
from byte.byte_account import account
from byte.byte_logger import log_keeper
from datetime import datetime
from prometheus_client import start_http_server, Gauge

parser = argparse.ArgumentParser()
parser.add_argument(
    "-I", "--interval", default=600, type=int, help="interval on which to scrape"
)
parser.add_argument(
    "-K", "--key", required=True, type=str, help="API Key for Bytesized Hosting"
)
parser.add_argument(
    "-U", "--url", default="https://bytesized-hosting.com/api/v1/accounts.json", type=str, help="url to accounts api"
)

# parse arguments into array
args = parser.parse_args()
interval = args.interval
api = args.key
url = args.url
params= {'api_key': api}

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
g_memory_usage = Gauge('bytesized_appbox_memory_usage', 'AppBox Memory Usage')
g_disk_quota = Gauge('bytesized_appbox_disk_usage', 'AppBox Disk Quota')
g_bandwidth_quota = Gauge('bytesized_appbox_bandwidth_usage', 'AppBox Bandwidth Quota')

def prom_gauge_set(metrics):
    g_memory_usage.set(metrics.memory_usage)
    g_disk_quota.set(metrics.disk_quota)
    g_bandwidth_quota.set(metrics.bandwidth_quota)

def main():
    try:
        response = requests.get(url, params=params)
        response_json = response.json()
        metrics = account(response_json, response.status_code)
    except requests.exceptions.RequestException as exception:
        raise SystemExit(logging.critical(exception))

    if metrics.response_code == 200:
        log_keeper.success(metrics)
        prom_gauge_set(metrics)

    elif metrics.response_code == 404:
        log_keeper.bad_key(metrics)
        pass


if __name__ == '__main__':
    try:
        start_http_server(8888, addr='0.0.0.0')
        logging.info('WEBSERVER STARTED SUCCESSFULLY: 0.0.0.0:8888\n\n')
        while True:
            main()
            time.sleep(interval)

    except OSError as error:
        SystemExit(logging.critical(error))