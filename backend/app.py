# app.py
from backend.db import barang_collection, gudang_collection, riwayat_collection
from backend.barang.barang import Barang
from backend.gudang.gudang import Gudang
from backend.riwayat.riwayat import Riwayat
from backend.status.status import Status
from typing import List

# mongo to object
def barang_from_mongo(json) -> Barang:
    barang = Barang(
        name=json["name"],
        capacity=json["capacity"],
        description=json["description"],
        gudang=json["gudang"]
    )
    barang._id = json["_id"]
    return barang

def gudang_from_mongo(json) -> Gudang:
    gudang = Gudang(
        gudang_name=json["gudang_name"],
        capacity=json["capacity"],
        max_capacity=json["max_capacity"],
        list_barang=json["list_barang"]
    )
    gudang._id = json["_id"]
    gudang.list_barang = json["list_barang"]
    return gudang

def riwayat_from_mongo(json) -> Riwayat:
    riwayat = Riwayat(
        value=json["value"],
        actionCode=json["actionCode"],
        timestamp=json["timestamp"],
        success=json["success"]
    )
    riwayat._id = json["_id"]
    return riwayat


# CRUD for Barang
# CREATE NEW BARANG
def create_barang(barang: Barang, gudang: Gudang, qty: int) -> int:
    
    highest_barang = barang_collection.find_one({}, sort=[("_id", -1)])

    if highest_barang is not None:
        barang._id = highest_barang["_id"] + 1
    else:
        barang._id = 1

    if gudang.capacity + barang.capacity * qty > gudang.max_capacity:
        print("Gudang capacity exceeded")
        return -1
    
    barang.gudang = [gudang._id]
    gudang.list_barang.append((barang._id, qty))

    document = {
        "_id": barang._id,
        "name": barang.name,
        "capacity": barang.capacity,
        "description": barang.description,
        "gudang": barang.gudang
    }
    result = barang_collection.insert_one(document)
    gudang_collection.update_one({"_id": gudang._id}, {"$set": {
        "list_barang": gudang.list_barang,
        "capacity" : calculate_current_capacity(gudang)
    }})
    return result.inserted_id

# ADD EXISTING BARANG TO GUDANG
def add_barang(barang: Barang, gudang: Gudang, jumlah: int) -> None:
    if gudang.capacity + barang.capacity * jumlah > gudang.max_capacity:
        print("Gudang capacity exceeded")
        return
    barang.gudang.append(gudang._id)
    gudang.list_barang.append((barang._id, jumlah))
    barang_collection.update_one({"_id": barang._id}, {"$set": {
        "gudang": barang.gudang
    }})
    gudang_collection.update_one({"_id": gudang._id}, {"$set": {
        "list_barang": gudang.list_barang
    }})
    print(f"Barang with ID {barang._id} added to Gudang with ID {gudang._id}")

def get_barang(_id: int) -> Barang:
    barang = barang_collection.find_one({"_id": _id})
    if barang is None:
        print("Barang not found")
        return None
    return barang_from_mongo(barang)

def get_barang_by_name(name: str) -> Barang:
    barang = barang_collection.find_one({"name": name})
    if barang is None:
        print("Barang not found")
        return None
    return barang_from_mongo(barang)

def get_barang_by_gudang(gudang: Gudang) -> List[Barang]:
    list_barang = []
    for barang_id, _ in gudang.list_barang:
        barang = get_barang(barang_id)
        print(f"Barang with ID {barang._id} and name {barang.name} found in Gudang with ID {gudang._id}")
        list_barang.append(barang)
    return list_barang

def get_all_barang() -> List[Barang]:
    barang = barang_collection.find()
    return [barang_from_mongo(b) for b in barang]

def update_barang(barang: Barang) -> None:
    previous_capacity = barang_collection.find_one({"_id": barang._id})["capacity"]
    barang_collection.update_one({"_id": barang._id}, {"$set": {
        "name": barang.name,
        "capacity": barang.capacity,
        "description": barang.description,
        "gudang": barang.gudang
    }})
    for gudang_id in barang.gudang:
        gudang = gudang_from_mongo(gudang_collection.find_one({"_id": gudang_id}))

        if calculate_current_capacity(gudang) > gudang.max_capacity:
            print("Gudang capacity exceeded")
            barang_collection.update_one({"_id": barang._id}, {"$set": {
                "capacity": previous_capacity
            }})
            return
        
        gudang_collection.update_one({"_id": gudang_id}, {"$set": {
            "capacity" : calculate_current_capacity(gudang),
            "list_barang": gudang.list_barang
        }})
        print(f"Gudang with ID {gudang_id} updated successfully")
    print(f"Barang with ID {barang._id} and name {barang.name} updated successfully")

def update_barang_qty(barang_id: int, gudang_id: int, qty: int) -> None:
    barang = get_barang(barang_id)
    gudang = get_gudang(gudang_id)
    for i in range(len(gudang.list_barang)):
        if gudang.list_barang[i][0] == barang._id:
            if qty <= 0:
                gudang.list_barang.pop(i)
                barang.gudang.remove(gudang._id)
                barang_collection.update_one({"_id": barang._id}, {"$set": {
                    "gudang": barang.gudang
                }})
                print(gudang.list_barang)

            else:
                gudang.list_barang[i] = (barang._id, qty)
            break
    if calculate_current_capacity(gudang) > gudang.max_capacity:
        print("Gudang capacity exceeded")
        return
    
    print(gudang.list_barang)
    
    gudang_collection.update_one({"_id": gudang._id}, {"$set": {
        "list_barang": gudang.list_barang,
        "capacity" : calculate_current_capacity(gudang)
    }})
    print(gudang.list_barang)

    print(f"Barang with ID {barang._id} updated successfully")

    

def delete_barang(_id: int) -> None:
    barang = barang_collection.find_one({"_id": _id})
    if barang is None:
        print("Barang not found")
        return
    for gudang_id in barang["gudang"]:
        gudang = gudang_from_mongo(gudang_collection.find_one({"_id": gudang_id}))
        gudang.list_barang = [b for b in gudang.list_barang if b[0] != _id]
        print(f"Barang with ID {_id} deleted from Gudang with ID {gudang_id}")

        gudang_collection.update_one({"_id": gudang_id}, {"$set": {
            "list_barang": gudang.list_barang,
            "capacity" : calculate_current_capacity(gudang)
        }})
    barang_collection.delete_one({"_id": _id})
    print(f"Barang with ID {_id} deleted successfully")

def remove_barang(barang: Barang, gudang: Gudang) -> None:
    barang.gudang.remove(gudang._id)
    gudang.list_barang = [b for b in gudang.list_barang if b[0] != barang._id]

    barang_collection.update_one({"_id": barang._id}, {"$set": {
        "gudang": barang.gudang
    }})
    gudang_collection.update_one({"_id": gudang._id}, {"$set": {
        "list_barang": gudang.list_barang,
        "capacity" : calculate_current_capacity(gudang)
    }})
    print(f"Barang with ID {barang._id} removed from Gudang with ID {gudang._id}")


# CRUD for Gudang
def calculate_current_capacity(gudang: Gudang) -> int:
    # if gudang.list_barang is None:
    #     return 0
    # return sum([get_barang(b[0]).capacity * b[1] for b in gudang.list_barang])
    sum = 0
    for barang_id, qty in gudang.list_barang:
        barang = get_barang(barang_id)
        if(barang is None):
            continue
        sum += barang.capacity * qty

    return sum
    
def create_gudang(gudang: Gudang) -> int:
    highest_gudang = gudang_collection.find_one({}, sort=[("_id", -1)])

    if highest_gudang is not None:
        gudang._id = highest_gudang["_id"] + 1
    else:
        gudang._id = 1

    document = {
        "_id": gudang._id,
        "gudang_name": gudang.gudang_name,
        "capacity": gudang.capacity,
        "max_capacity": gudang.max_capacity,
        "list_barang": gudang.list_barang
    }
    result = gudang_collection.insert_one(document)
    print(f"Gudang with ID {gudang._id} created successfully")
    return result.inserted_id

def get_gudang(_id: int) -> Gudang:
    gudang = gudang_collection.find_one({"_id": _id})
    if gudang is None:
        print("Gudang not found")
        return None
    return gudang_from_mongo(gudang)

def get_gudang_by_name(gudang_name: str) -> Gudang:
    gudang = gudang_collection.find_one({"gudang_name": gudang_name})
    if gudang is None:
        print("Gudang not found")
        return None
    return gudang_from_mongo(gudang)

def search_barang_in_gudang(gudang_id: int, barang_name: str) -> List[Barang]:
    gudang = get_gudang(gudang_id)
    barang_list = []
    for barang_id, _ in gudang.list_barang:
        barang = get_barang(barang_id)
        if barang.name == barang_name:
            print(f"Barang with name {barang_name} found in Gudang with ID {gudang._id}")
            barang_list.append(barang)
    return barang_list

def get_all_gudang() -> List[Gudang]:
    gudang = gudang_collection.find()
    return [gudang_from_mongo(g) for g in gudang]

def update_gudang(gudang: Gudang) -> int:
    if calculate_current_capacity(gudang) > gudang.max_capacity:
        print("Gudang capacity exceeded")
        return -1
    
    gudang_capacity = calculate_current_capacity(gudang)
    
    gudang_collection.update_one({"_id": gudang._id}, {"$set": {
        "gudang_name": gudang.gudang_name,
        "capacity": gudang_capacity,
        "max_capacity": gudang.max_capacity,
        "list_barang": gudang.list_barang
    }})
    print(f"Gudang with ID {gudang._id} and name {gudang.gudang_name} updated successfully")
    return 1

def delete_gudang(_id: int) -> None:
    gudang = gudang_collection.find_one({"_id": _id})
    if gudang is None:
        print("Gudang not found")
        return
    for barang_id, _ in gudang["list_barang"]:
        barang = barang_collection.find_one({"_id": barang_id})
        barang.gudang.remove(_id)
        barang_collection.update_one({"_id": barang_id}, {"$set": {
            "gudang": barang.gudang
        }})
    gudang_collection.delete_one({"_id": _id})
    print(f"Gudang with ID {_id} deleted successfully")

def pindah_barang(barang_id: int, source_gudang_id: int, dest_gudang_id: int, qty: int) -> Status:
    """
    Move barang from source Gudang to destination Gudang
    """
    barang = get_barang(barang_id)
    source_gudang = get_gudang(source_gudang_id)
    dest_gudang = get_gudang(dest_gudang_id)
    
    if not barang or not source_gudang or not dest_gudang:
        return Status.error(message="Barang or Gudang not found")
    
    # Check if barang exists in source Gudang
    source_qty = 0
    for b_id, quantity in source_gudang.list_barang:
        if b_id == barang_id:
            source_qty = quantity
            break
    
    if source_qty < qty:
        return Status.error(message=f"Insufficient quantity in source Gudang. Available: {source_qty}, Requested: {qty}")
    
    # Check if destination Gudang has enough capacity
    if dest_gudang.capacity + (barang.capacity * qty) > dest_gudang.max_capacity:
        return Status.error(message="Destination Gudang doesn't have enough capacity")
    
    # Remove from source Gudang
    update_barang_qty(barang_id, source_gudang_id, source_qty - qty)
    
    # Add to destination Gudang
    # Check if barang already exists in destination Gudang
    dest_qty = 0
    found = False
    for b_id, quantity in dest_gudang.list_barang:
        if b_id == barang_id:
            dest_qty = quantity
            found = True
            break
    if not found:
        added = get_barang(barang_id)
        add_barang(added, dest_gudang, qty)
        print(f"NAMBAH {dest_gudang._id}")
    else :
        update_barang_qty(barang_id, dest_gudang_id, dest_qty + qty)
    
    # if dest_qty > 0:
    #     update_barang_qty(barang_id, dest_gudang_id, dest_qty + qty)

    # else:
    #     # If barang doesn't exist in destination Gudang yet
    #     dest_gudang.list_barang.append((barang_id, qty))
    #     barang.gudang.append(dest_gudang_id)
        
    #     barang_collection.update_one({"_id": barang_id}, {"$set": {
    #         "gudang": barang.gudang
    #     }})
    #     gudang_collection.update_one({"_id": dest_gudang_id}, {"$set": {
    #         "list_barang": dest_gudang.list_barang,
    #         "capacity": calculate_current_capacity(dest_gudang)
    #     }})
# CRUD for Riwayat
# ga yakin riwayat ini bener
def create_riwayat(Riwayat) -> None:
    highest_riwayat = riwayat_collection.find_one({}, sort=[("_id", -1)])
    Riwayat._id = 1 if highest_riwayat is None else highest_riwayat["_id"] + 1
    document = {
        "_id": Riwayat._id,
        "value": Riwayat.value,
        "actionCode": Riwayat.actionCode,
        "timestamp": Riwayat.time,
        "success": Riwayat.success
    }
    result = riwayat_collection.insert_one(document)
    print(f"Riwayat with ID {Riwayat._id} created successfully")
    return result.inserted_id

# TESTING
# a = BarangManager()
# s = Status()
# s = a.pindahBarang()
# gudang1 = Gudang("Gudang 1", 0, 1000, [])
# gudang2 = Gudang("Gudang 2", 0, 1000, [])
# create_gudang(gudang1)
# create_gudang(gudang2)
# barang1 = Barang("Barang 1", 10, "Barang pertama", [])
# barang2 = Barang("Barang 2", 20, "Barang kedua", [])
# tempgudang = get_gudang(1)
# create_barang(barang1, tempgudang, 10)
# tempgudang = get_gudang(2)
# create_barang(barang2, tempgudang, 20)
# tempbarang = get_barang(1)
# tempgudang = get_gudang(1)
# gudang1 = get_gudang(1)
# print(gudang1.list_barang)
# gudang1 = get_gudang(1)
# print(gudang1.list_barang)
# tempbarang = get_barang(1)
# tempbarang.name = "Barang 1 Updated"
# update_barang(tempbarang)
# gudang1 = get_gudang(1)
# print(gudang1.list_barang)
# barang3 = Barang("Barang 3", 30, "Barang ketiga", [])
# create_barang(barang3, tempgudang, 30)
# gudang1 = get_gudang(1)
# print(gudang1.list_barang)
# riwayat = Riwayat(1, "CREATE", "2021-08-01", True)
# create_riwayat(riwayat)
