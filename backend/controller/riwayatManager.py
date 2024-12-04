import json
import os
from datetime import datetime
from ..riwayat.riwayat import Riwayat

class RiwayatManager:
    def __init__(self):
        self.riwayat_list = []
        self.load_data()

    def load_data(self):
        if os.path.exists("riwayat.json"):
            with open("riwayat.json", "r") as file:
                data = json.load(file)
                for riwayat in data:
                    self.riwayat_list.append(Riwayat(riwayat["value"], riwayat["actionCode"], riwayat["time"], riwayat["success"]))
                    
    def save_data(self):
        with open("riwayat.json", "w") as file:
            data = []
            for riwayat in self.riwayat_list:
                data.append({"value": riwayat.get_value(), "actionCode": riwayat.get_actionCode(), "time": riwayat.get_time(), "success": riwayat.get_success()})
            json.dump(data, file)

    def add_riwayat(self, value: int, action_code: str, success: bool):
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        riwayat = Riwayat(value, action_code, time, success)
        self.riwayat_list.append(riwayat)
        self.save_data()
