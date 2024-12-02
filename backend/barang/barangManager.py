from typing import List

class Barang:
    def __init__(self, name: str, capacity: int, description: str, gudang: List[int]):
        self._id = 0
        self.name = name
        self.capacity = capacity
        self.description = description
        self.gudang = gudang