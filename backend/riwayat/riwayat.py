class Riwayat:
    def __init__(self, value, actionCode, timestamp, success):
        self._id = 0
        self.value = value
        self.actionCode = actionCode
        self.timestamp = timestamp
        self.success = success

    def display(self):
        print(f"Value: {self.value}, Action Code: {self.actionCode}, Timestamp: {self.timestamp}, Success: {self.success}")