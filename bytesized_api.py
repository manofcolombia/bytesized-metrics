import requests
import json
import time
import sys
import argparse
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

g_bytesized_appbox_memory_usage = Gauge('bytesized_appbox_memory_usage', 'AppBox Memory Usage')
g_bytesized_appbox_disk_quota = Gauge('bytesized_appbox_disk_usage', 'AppBox Disk Quota')
g_bytesized_appbox_bandwidth_quota = Gauge('bytesized_appbox_bandwidth_usage', 'AppBox Bandwidth Quota')

def main():
    response = requests.get(url, params=params)

    if response.status_code == 200:
        response_json = response.json()
        metrics = account(response_json)
        log_keeper.success(metrics)
        g_bytesized_appbox_memory_usage.set(metrics.memory_usage)
        g_bytesized_appbox_disk_quota.set(metrics.disk_quota)
        g_bytesized_appbox_bandwidth_quota.set(metrics.bandwidth_quota)

    elif response.status_code == 404:
        sys.stderr.write(str(response))
        sys.stderr.write('\nRequest to api failed.\nPlease verify you have the correct api key.')
        pass
    else:
        sys.stderr.write('API unreachable. Verify network reachability ' + str(response) + '\n\n')
        pass

if __name__ == '__main__':
    try:
        start_http_server(8888, addr='0.0.0.0')
        sys.stdout.write('WEBSERVER STARTED SUCCESSFULLY: 0.0.0.0:8888\n\n')
        while True:
            main()
            time.sleep(interval)

    except:
        sys.stderr.write('Webserver failed to start. Verify port is not in use')
        exit()