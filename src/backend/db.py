from pymongo import MongoClient
from dotenv import load_dotenv
import os
from frontend.const import DARK_TEXT

# Load environment variables
load_dotenv()
mongo_uri = "mongodb://localhost:27017/"

client = MongoClient(mongo_uri)
db = client['storage_allocation_manager']
gudang_collection = db['gudang']
barang_collection = db['barang']
riwayat_collection = db['riwayat']

# Perform a simple query to check the connection
try:
    # List the databases to confirm connection
    databases = client.list_database_names()
    print("Connected to MongoDB!")
    print("Databases:", databases)
except Exception as e:
    print("Failed to connect to MongoDB:", e)
