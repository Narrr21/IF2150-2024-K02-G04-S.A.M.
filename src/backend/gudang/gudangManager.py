from typing import List, Tuple
from backend.controller.riwayatManager import RiwayatManager
from backend.gudang import Gudang
from backend.app import get_gudang, create_gudang, delete_gudang, update_gudang, get_barang_by_gudang, update_barang_qty

class GudangManager:
    def __init__(self):
        pass

    def changeName(id: int, nama: str):
        target = get_gudang(id)
        target.gudang_name = nama
        update_gudang(target)

    def changeMaxCapacity(id: int, cap: int):
        target = get_gudang(id)
        target.max_capacity = cap
        update_gudang(target)
    
    def createGudang(gudang_name: str, capacity: int,max_capacity: int, list_barang: List[Tuple[int, int]]):
        Gudang.gudang_name = gudang_name
        Gudang.capacity = capacity
        Gudang.max_capacity = max_capacity
        if list_barang is None:
            Gudang.list_barang = []
        else:
            Gudang.list_barang = list_barang
        create_gudang(Gudang)
    
    def deleteGudang(id: int):
        delete_gudang(id)
    
    def openGudang(id: int):
        target = get_gudang(id)
        list_barang = get_barang_by_gudang(target)
        return list_barang

    def changeQuantity(gudang_id: int, barang_id: int, quantity: int):
        update_barang_qty(barang_id, gudang_id, quantity)

    def __saveHistory(act: str, targetid: int, success: bool):
        if not success:
            RiwayatManager.create_riwayat_loc([targetid], act, False)
            return
        
        if act == "CG":
            RiwayatManager.create_riwayat_loc([targetid], act, True)
        elif act == "DG":
            RiwayatManager.create_riwayat_loc([targetid], act, True)
        elif act == "UG":
            RiwayatManager.create_riwayat_loc([targetid], act, True)

        




        