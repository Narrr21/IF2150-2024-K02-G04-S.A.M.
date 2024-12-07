from barang import Barang
from riwayat.riwayatManager import create_riwayat_loc
from typing import List
from app import *

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
            create_riwayat_loc(value, act, False)
            return
        if act == "CB":
            create_riwayat_loc(value, act, True)
        elif act == "DB":
            create_riwayat_loc(value, act, True)
        elif act == "UB":
            create_riwayat_loc(value, act, True)
        elif act == "PB":
            create_riwayat_loc(value, act, True)
            
    # def moveBarang(id_barang:int, id_gudang:int):