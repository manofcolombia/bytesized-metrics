from datetime import date
class account:
    def __init__ (self, response_json, response_code):
        self.response_code = response_code

        if self.response_code == 200:
            self.response_json = response_json
            self.server_name = self.response_json[0]['server_name']
            self.disk_quota = self.response_json[0]['disk_quota']
            self.bandwidth_quota = self.response_json[0]['bandwidth_quota']
            self.memory_usage = self.response_json[0]['memory_usage']
            self.paid_till = date.fromisoformat(self.response_json[0]['paid_till'])
            self.days_paid_till = (self.paid_till - date.today()).days