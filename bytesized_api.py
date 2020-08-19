import prometheus_client
import requests
import json
import argparse
import logging
from byte.byte_account import account
from byte.byte_logger import log_keeper
from flask import Response, Flask
from multiprocessing import Process
from prometheus_client import Gauge, generate_latest

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

app = Flask(__name__)

@app.route('/metrics')
def main():
    try:
        args = byte_parser()
        url = args.url
        params = {'api_key': args.key}
        response = requests.get(url, params=params)
        response_json = response.json()
        metrics = account(response_json, response.status_code)
    except requests.exceptions.RequestException as exception:
        logging.critical(exception)
        return str(exception)

    if metrics.response_code == 200:
        log_keeper.success(metrics)
        gauges = prom_gauge_set(metrics)
        res = []
        for k,v in gauges.items():
            res.append(prometheus_client.generate_latest(v))
        return Response(res,mimetype="text/plain")

    elif metrics.response_code != 200:
        return log_keeper.bad_key(metrics)

def byte_parser():
    byte_parser = argparse.ArgumentParser()
    byte_parser.add_argument(
            "-K", "--key", required=True, type=str, help="API Key for Bytesized Hosting"
        )
    byte_parser.add_argument(
            "-U", "--url", default="https://bytesized-hosting.com/api/v1/accounts.json", type=str, help="url to accounts api"
        )
    byte_parsed = byte_parser.parse_args()
    return byte_parsed

def prom_gauge_set(metrics):
    gauges = {}
    gauges['memory_usage'] = Gauge('bytesized_memory_usage', 'AppBox Memory Usage')
    gauges['disk_quota'] = Gauge('bytesized_disk_usage', 'AppBox Disk Quota')
    gauges['bandwidth_quota'] = Gauge('bytesized_bandwidth_usage', 'AppBox Bandwidth Quota')
    gauges['memory_usage'].set(metrics.memory_usage)
    gauges['disk_quota'].set(metrics.disk_quota)
    gauges['bandwidth_quota'].set(metrics.bandwidth_quota)
    return gauges

if __name__ == "__main__":
    try:
        app.run(host='0.0.0.0', port=8888)
    except OSError as error:
        SystemExit(logging.critical(error))