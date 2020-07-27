import requests
import json
import time
import sys
import argparse
from prometheus_client import start_http_server, Gauge

parser = argparse.ArgumentParser()
parser.add_argument(
    "-I", "--interval", required=True, type=int, help="interval on which to scrape"
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

g_memory_usage = Gauge('memory_usage', 'AppBox Memory Usage')
g_disk_quota = Gauge('disk_usage', 'AppBox Disk Quota')
g_bandwidth_quota = Gauge('bandwidth_usage', 'AppBox Bandwidth Quota')

def get_byte_stats():
    response = requests.get(url, params=params)
    response_json = response.json()
    server_name = response_json[0]['server_name']
    disk_quota = response_json[0]['disk_quota']
    bandwidth_quota = response_json[0]['bandwidth_quota']
    memory_usage = response_json[0]['memory_usage']

    if response.status_code == 200:
        sys.stdout.write(str(response) + '\n')
        sys.stdout.write('SERVER_NAME: ' + server_name + '\n')
        sys.stdout.write('MEMORY_USAGE: ' + str(memory_usage) + '\n')
        sys.stdout.write('DISK_QUOTA: ' + str(disk_quota) + '\n')
        sys.stdout.write('BANDWIDTH_QUOTA: ' + str(bandwidth_quota) + '\n\n')
        g_memory_usage.set(memory_usage)
        g_disk_quota.set(disk_quota)
        g_bandwidth_quota.set(bandwidth_quota)
    
    else:
        sys.stderr.write('Request failed ' + str(response) + '\n\n')

if __name__ == '__main__':
    start_http_server(8888, addr='0.0.0.0')
    while True:
        get_byte_stats()
        time.sleep(interval)
