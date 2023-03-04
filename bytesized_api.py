"""Bytesized prometheus exporter"""
import argparse
import logging
import time
import sys
from datetime import date
import cloudscraper
import requests
from prometheus_client import start_http_server
from prometheus_client.core import GaugeMetricFamily, REGISTRY

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

class ByteCollector():
    '''Custom Prometheus collector for bytesized appboxes'''

    def __init__(self):
        self.args = byte_parser()
        self.url = self.args.url
        self.params = {'api_key': self.args.key}

    def collect(self):
        '''Organize metrics'''

        try:
            scrapper = cloudscraper.create_scraper(delay=10, browser="chrome")
            response = scrapper.get(url=self.url, params=self.params)
            # response = requests.get(self.url, params=self.params)
            if response.status_code != 200:
                logging.info(f'Response Code: {response.status_code}')
                logging.info("Request to api failed. Please verify you have the correct api key.")
                sys.exit()
            else:
                response_json = response.json()

        except requests.exceptions.RequestException as exception:
            logging.critical(exception)
            print(str(exception))

        for appbox in response_json:
            server_name = appbox['server_name']
            memory_usage = appbox['memory_usage']
            disk_quota = appbox['disk_quota']
            bandwidth_quota = appbox['bandwidth_quota']
            paid_till = date.fromisoformat(appbox['paid_till'])
            next_payment = (paid_till - date.today()).days

            memory_usage_gauge = GaugeMetricFamily(
                "bytesized_memory_usage", 'AppBox Memory Usage', labels=['appbox']
                )
            memory_usage_gauge.add_metric([server_name], memory_usage)
            yield memory_usage_gauge

            disk_quota_gauge = GaugeMetricFamily(
                "bytesized_disk_quota", 'AppBox Disk Usage', labels=['appbox']
                )
            disk_quota_gauge.add_metric([server_name], disk_quota)
            yield disk_quota_gauge

            bandwidth_quota_gauge = GaugeMetricFamily(
                "bytesized_bandwidth_quota", 'AppBox Bandwidth Usage', labels=['appbox']
                )
            bandwidth_quota_gauge.add_metric([server_name], bandwidth_quota)
            yield bandwidth_quota_gauge

            next_payment_gauge = GaugeMetricFamily(
                "bytesized_next_payment", 'AppBox Payment Due in Days', labels=['appbox']
                )
            next_payment_gauge.add_metric([server_name], next_payment)
            yield next_payment_gauge

            logging.info(
                f"""
                    Response Header Date: {response.headers['Date']}
                    Response Code: {response.status_code}
                    Server Name: {server_name}
                    Memory Usage: {memory_usage}
                    Disk Quota: {disk_quota}
                    Bandwidth Quota: {bandwidth_quota}
                    Days till Next Payment: {next_payment}
                """
            )

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

if __name__ == "__main__":
    start_http_server(8888)
    REGISTRY.register(ByteCollector())
    while True:
        time.sleep(1)
