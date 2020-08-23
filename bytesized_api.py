"""Bytesized prometheus exporter"""
import argparse
import logging
import prometheus_client
import requests
from flask import Response, Flask
from prometheus_client import Gauge
from byte.byte_account import account
from byte.byte_logger import log_keeper

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

app = Flask(__name__)

gauges = {}
gauges['memory_usage'] = Gauge('bytesized_memory_usage', 'AppBox Memory Usage')
gauges['disk_quota'] = Gauge('bytesized_disk_usage', 'AppBox Disk Quota')
gauges['bandwidth_quota'] = Gauge('bytesized_bandwidth_usage', 'AppBox Bandwidth Quota')
gauges['days_paid_till'] = Gauge('bytesized_days_paid_till', 'AppBox Days till next payment')

@app.route('/metrics')
def main():
    """Main function"""
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
        gauges_set = prom_gauge_set(metrics)
        res = []
        for attr, value in gauges_set.items():
            res.append(prometheus_client.generate_latest(value))
            logging.debug(attr)
        return Response(res, mimetype="text/plain")

    return log_keeper.bad_key(metrics)

def byte_parser():
    """Parse args"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-K", "--key", required=True, type=str, help="API Key for Bytesized Hosting"
        )
    parser.add_argument(
        "-U", "--url", default="https://bytesized-hosting.com/api/v1/accounts.json",
        type=str, help="url to accounts api"
        )
    parsed = parser.parse_args()
    return parsed

def prom_gauge_set(metrics):
    """Set and return prom gauges with valid metrics"""
    gauges['memory_usage'].set(metrics.memory_usage)
    gauges['disk_quota'].set(metrics.disk_quota)
    gauges['bandwidth_quota'].set(metrics.bandwidth_quota)
    gauges['days_paid_till'].set(metrics.days_paid_till)
    return gauges

if __name__ == "__main__":
    try:
        app.run(host='0.0.0.0', port=8888)
    except OSError as error:
        SystemExit(logging.critical(error))
