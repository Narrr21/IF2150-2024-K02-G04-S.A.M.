from typing import List
from app import *
class Barang:
    def __init__(self, name: str, capacity: int, description: str, gudang: List[int]):
        self._id = 0
        self.name = name
        self.capacity = capacity
        self.description = description
        self.gudang = gudang

    def getID(self) -> int:
        return self._id
    
    def getName(self) -> str:
        return self.name
    
    def setName(self, new_name: str):
        self.name = new_name
    
    def getDeskripsi(self) -> str:
        return self.description
    
    def setDeskripsi(self, desc: str):
        self.description = desc

    def getCapacity(self) -> int:
        return self.capacity
    
    def setCapacity(self, cap: int):
        self.capacity = cap


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
        