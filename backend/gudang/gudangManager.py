from typing import List, Tuple, Optional
from barang.barangManager import Barang
from gudang import Gudang
from app import *

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
    
    def createGudang(gudang_name: str, capacity: int,max_capacity: int, list_barang: List[Tuple[Barang, int]]):
        gudang.gudang_name = gudang_name
        gudang.capacity = capacity
        gudang.max_capacity = max_capacity
        if list_barang is None:
            gudang.list_barang: List[Tuple[Barang, int]] = []
        else:
            gudang.list_barang = list_barang
        create_gudang(gudang)
    
    def deleteGudang(id: int):
        delete_gudang(id)
    
    def 



        