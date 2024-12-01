# app.py
from db import collection

def insert_data():
    document = {"name": "Alice", "email": "alice@example.com", "age": 30}
    result = collection.insert_one(document)
    print(f"Inserted document ID: {result.inserted_id}")

def fetch_data():
    documents = collection.find()
    print("Documents in the collection:")
    for doc in documents:
        print(doc)

def update_data():
    query = {"name": "Alice"}
    update = {"$set": {"age": 35}}
    result = collection.update_one(query, update)
    print(f"Matched {result.matched_count}, Modified {result.modified_count}")

def delete_data():
    query = {"name": "Alice"}
    result = collection.delete_one(query)
    print(f"Deleted {result.deleted_count} document(s)")

# Main execution
if __name__ == "__main__":
    print("Running MongoDB operations...")
    insert_data()
    fetch_data()
    update_data()
    delete_data()