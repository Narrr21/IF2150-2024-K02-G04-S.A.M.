from typing import List,Optional

class Gudang:
    def __init__(self, gudang_name: str, capacity: int,max_capacity: int):
        '''
        Initialisa a Gudang entity.
        @param gudang_name: Name of the Gudang(Storage).
        @param capacity: Gudang(Storage) capacity currently.
        @param max_capacity: Maximum capacity of Gudang(Storage).
        '''
        self.gudang_name = gudang_name
        self.capacity = capacity
        self.max_capacity = max_capacity
        self.list_barang: List[Barang] = []