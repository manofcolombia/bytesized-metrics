import logging

class log_keeper:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
    
    def __init__(self, metrics):
        self.metrics = metrics
        self.response_code = self.metrics.response_code
        self.server_name = self.metrics.server_name
        self.memory_usage = self.metrics.memory_usage
        self.disk_quota = self.metrics.disk_quota
        self.bandwidth_quota = self.metrics.bandwidth_quota
        self.days_paid_till = self.metrics.days_paid_till

    def success(self):

        logging.info(
            f"""
                Response Code: {self.response_code}
                Server Name: {self.server_name}
                Memory Usage: {self.memory_usage}
                Disk Quota: {self.disk_quota}
                Bandwidth Quota: {self.bandwidth_quota}
                Days till Next Payment: {self.days_paid_till}
            """
        )

    def bad_key(self):
        logging.info("Response Code: " + str(self.response_code))
        logging.info("Request to api failed. Please verify you have the correct api key.")
        return "Response Code: " + str(self.response_code) + " Request to api failed. Please verify you have the correct api key."