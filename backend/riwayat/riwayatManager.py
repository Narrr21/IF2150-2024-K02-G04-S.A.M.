import json
import os
from datetime import datetime
from typing import List, Tuple
from riwayat import Riwayat

class RiwayatManager:
    def __init__(self):
        self.riwayat_file = os.path.join(os.path.dirname(__file__), "riwayat.json")
        self._init_storage()

    def _init_storage(self) -> None:
        # Create riwayat.json if it doesn't exist
        if not os.path.exists(self.riwayat_file):
            with open(self.riwayat_file, 'w') as f:
                json.dump([], f)

    def _load_riwayat(self) -> List[Riwayat]:
        # Load riwayat data from JSON file
        with open(self.riwayat_file, 'r') as f:
            return json.load(f)

    def _save_riwayat(self, riwayat: List[Riwayat]) -> None:
        # Save riwayat data to JSON file
        with open(self.riwayat_file, 'w') as f:
            json.dump(riwayat, f, indent=4)

    def add_riwayat(self, value: List[int], actionCode: str, success: bool) -> Tuple[bool, str]:
        try:
            dataRiwayat = self._load_riwayat()
            new_riwayat = Riwayat(value, actionCode, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), success)
            dataRiwayat.append(new_riwayat)
            self._save_riwayat(dataRiwayat)
            return True, "Riwayat added successfully"
        except Exception as e:
            return False, f"Failed to add riwayat: {str(e)}"

    def get_all_riwayat(self) -> Tuple[bool, List[Riwayat], str]:
        try:
            riwayat = self._load_riwayat()
            return True, riwayat, "Riwayat loaded successfully"
        except Exception as e:
            return False, [], f"Failed to load riwayat: {str(e)}"

    def delete_riwayat(self, idRiwayat: int) -> Tuple[bool, str]:
        try:
            riwayat = self._load_riwayat()
            updated_riwayat = [r for r in riwayat if r["idRiwayat"] != idRiwayat]
            if len(riwayat) == len(updated_riwayat):
                return False, f"Riwayat with ID {idRiwayat} not found"
            self._save_riwayat(updated_riwayat)
            return True, "Riwayat deleted successfully"
        except Exception as e:
            return False, f"Failed to delete riwayat: {str(e)}"
