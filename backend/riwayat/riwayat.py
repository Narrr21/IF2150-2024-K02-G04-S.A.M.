class Riwayat:
    def __init__(self, value, actionCode, time, success):
        self._id = 0
        self.value = value
        self.actionCode = actionCode
        self.time = time
        self.success = success

    def display(self):
        print(f"Value: {self.value}, Action Code: {self.actionCode}, Time: {self.time}, Success: {self.success}")