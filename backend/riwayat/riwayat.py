class Riwayat:
    def __init__(self, value, actionCode, time, success):
        self.value = value
        self.actionCode = actionCode
        self.time = time
        self.success = success
    def get_value(self):
        return self.value
    def get_actionCode(self):
        return self.actionCode
    def get_time(self):
        return self.time
    def get_success(self):
        return self.success
    def set_value(self, value):
        self.value = value
    def set_actionCode(self, actionCode):
        self.actionCode = actionCode
    def set_time(self, time):
        self.time = time
    def set_success(self, success):
        self.success = success
    def display(self):
        return f"Value: {self.value}, Action Code: {self.actionCode}, Time: {self.time}, Success: {self.success}"