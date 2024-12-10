from datetime import datetime
from typing import List
from backend.riwayat.riwayat import Riwayat
from backend.app import create_riwayat, riwayat_from_mongo, riwayat_collection

class RiwayatManager:
    def __init__(self):
        pass

    def create_riwayat_loc(value: List[int], actionCode: int, success: bool) -> int:
        riwayat = Riwayat(
            value=value,
            actionCode=actionCode,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            success=success
        )
        id = create_riwayat(riwayat)
        return id
    
    @staticmethod
    def get_riwayat(_id: int) -> Riwayat:
        riwayat = riwayat_collection.find_one({"_id": _id})
        if riwayat is None:
            print("Riwayat not found")
            return None
        return riwayat_from_mongo(riwayat)
    
    @staticmethod
    def get_all_riwayat() -> List[Riwayat]:
        riwayat = riwayat_collection.find()
        return [riwayat_from_mongo(r) for r in riwayat]
    
    @staticmethod
    def translate_riwayat(_id: int) -> str:
        riwayat = RiwayatManager.get_riwayat(_id)
        if riwayat is None:
            return "Riwayat not found"
        if riwayat.actionCode == "CB":
            return f"Barang with ID {riwayat.value[0]} created in gudang with ID {riwayat.value[1]}"
        elif riwayat.actionCode == "DB":
            return f"Barang with ID {riwayat.value[0]} deleted from gudang with ID {riwayat.value[1]}"
        elif riwayat.actionCode == "UB":
            return f"Barang with ID {riwayat.value[0]} updated"
        elif riwayat.actionCode == "PB":
            return f"Barang with ID {riwayat.value[0]} moved to Gudang with ID {riwayat.value[1]} from Gudang with ID {riwayat.value[2]} in quantity {riwayat.value[3]}"
        elif riwayat.actionCode == "CG":
            return f"Gudang with ID {riwayat.value[0]} created"
        elif riwayat.actionCode == "DG":
            return f"Gudang with ID {riwayat.value[0]} deleted"
        elif riwayat.actionCode == "UG":
            return f"Gudang with ID {riwayat.value[0]} updated"