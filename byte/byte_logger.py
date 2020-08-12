import logging

class log_keeper:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
    
    def __init__(self, metrics):
        self.metrics = metrics
        self.server_name = self.metrics.server_name
        self.memory_usage = self.metrics.memory_usage
        self.disk_quota = self.metrics.disk_quota
        self.bandwidth_quota = self.metrics.bandwidth_quota



    def success(self):
        logging.info(
            f"""
                Server Name: {self.server_name}
                Memory Usage: {self.memory_usage}
                Disk Quota: {self.disk_quota}
                Bandwidth Quota: {self.bandwidth_quota}
            """
        )

    def bad_key(self):
        logging.info("Request to api failed.\nPlease verify you have the correct api key.")