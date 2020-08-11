class account:
    def __init__ (self, response_json):
        self.response_json = response_json
        self.server_name = self.response_json[0]['server_name']
        self.disk_quota = self.response_json[0]['disk_quota']
        self.bandwidth_quota = self.response_json[0]['bandwidth_quota']
        self.memory_usage = self.response_json[0]['memory_usage']