from typing import List,Optional

class Gudang:
    def __init__(self, nama_gudang: str, capacity: int,max_capacity: int):
        '''
        Initialize a Gudang entity.
        @param nama_gudang: Nama dari gudang.
        @param capacity: Kapasitas gudang saat ini.
        @param max_capacity: Kapasitas maksimum dari gudang.
        '''
        self.nama_gudang = nama_gudang
        self.capacity = capacity
        self.max_capacity = max_capacity
        self.list_barang: List[Barang] = []