"""Bytesized prometheus exporter"""
import argparse
import logging
import time
import sys
from datetime import date
import requests
from prometheus_client import start_http_server
from prometheus_client.core import GaugeMetricFamily, REGISTRY

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

class ByteCollector():
    '''Custom Prometheus collector for bytesized appboxes'''

    def __init__(self):
        try:
            self.args = byte_parser()
            self.url = self.args.url
            self.params = {'api_key': self.args.key}
            self.response = requests.get(self.url, params=self.params)
            if self.response.status_code != 200:
                logging.info(f'Response Code: {self.response.status_code}')
                logging.info("Request to api failed. Please verify you have the correct api key.")
                sys.exit()
            else:
                self.response_json = self.response.json()

        except requests.exceptions.RequestException as exception:
            logging.critical(exception)
            print(str(exception))

    def collect(self):
        '''Organize metrics'''

        for appbox in self.response_json:
            self.server_name = appbox['server_name']
            self.memory_usage = appbox['memory_usage']
            self.disk_quota = appbox['disk_quota']
            self.bandwidth_quota = appbox['bandwidth_quota']
            self.paid_till = date.fromisoformat(appbox['paid_till'])
            self.next_payment = (self.paid_till - date.today()).days

            self.memory_usage_gauge = GaugeMetricFamily(
                "memory_usage", 'AppBox Memory Usage', labels=['appbox']
                )
            self.memory_usage_gauge.add_metric([self.server_name], self.memory_usage)
            yield self.memory_usage_gauge

            self.disk_quota_gauge = GaugeMetricFamily(
                "disk_quota", 'AppBox Disk Usage', labels=['appbox']
                )
            self.disk_quota_gauge.add_metric([self.server_name], self.disk_quota)
            yield self.disk_quota_gauge

            self.bandwidth_quota_gauge = GaugeMetricFamily(
                "bandwidth_quota", 'AppBox Bandwidth Usage', labels=['appbox']
                )
            self.bandwidth_quota_gauge.add_metric([self.server_name], self.bandwidth_quota)
            yield self.bandwidth_quota_gauge

            self.next_payment_gauge = GaugeMetricFamily(
                "next_payment", 'AppBox Payment Due in Days', labels=['appbox']
                )
            self.next_payment_gauge.add_metric([self.server_name], self.next_payment)
            yield self.next_payment_gauge

            logging.info(
                f"""
                    Response Code: {self.response.status_code}
                    Server Name: {self.server_name}
                    Memory Usage: {self.memory_usage}
                    Disk Quota: {self.disk_quota}
                    Bandwidth Quota: {self.bandwidth_quota}
                    Days till Next Payment: {self.next_payment}
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
