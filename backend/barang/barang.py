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
