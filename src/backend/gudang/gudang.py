from typing import List, Tuple

class Gudang:
    def __init__(self, gudang_name: str, capacity: int,max_capacity: int, list_barang: List[Tuple[int, int]]):
        '''
        Initialisa a Gudang entity.
        @param gudang_name: Name of the Gudang(Storage).
        @param capacity: Gudang(Storage) capacity currently.
        @param max_capacity: Maximum capacity of Gudang(Storage).
        '''
        self._id = 0
        self.gudang_name = gudang_name
        self.capacity = capacity
        self.max_capacity = max_capacity
        if list_barang is None:
            self.list_barang: List[Tuple[int, int]] = []
        else:
            self.list_barang = list_barang