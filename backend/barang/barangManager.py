from barang import Barang
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
    
    # def moveBarang(id_barang:int, id_gudang:int):