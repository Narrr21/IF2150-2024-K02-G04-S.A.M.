from backend.controller.riwayatManager import RiwayatManager 
from typing import List
from backend.app import *

class BarangManager:
    def __init__(self):
        pass

    def changeDeskripsi(id: int, desc:str):
        target = get_barang(id)
        target.setDeskripsi(desc)
        update_barang(target)

    def changeCapacity(id: int, cap: int):
        target = get_barang(id)
        target.setCapacity(cap)
        update_barang(target)
    
    def getByID(id: int):
        get_barang(id)

    def getByName(name: str):
        get_barang_by_name(name)
    
    def __saveHistory(act: str, value: List, success: bool):
        if not success:
            RiwayatManager.create_riwayat_loc(value, act, False)
            return
        if act == "CB":
            RiwayatManager.create_riwayat_loc(value, act, True)
        elif act == "DB":
            RiwayatManager.create_riwayat_loc(value, act, True)
        elif act == "UB":
            RiwayatManager.create_riwayat_loc(value, act, True)
        elif act == "PB":
            RiwayatManager.create_riwayat_loc(value, act, True)
            
    # def moveBarang(id_barang:int, id_gudang:int):