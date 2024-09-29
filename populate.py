from pymongo import MongoClient
import hashlib
import random
import datetime

client = MongoClient('mongodb://localhost:27017/')
db = client['inventory_db']
items_collection = db['items']
users_collection = db['users']

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_users():
    user_roles = ['admin', 'user']
    for i in range(1, 21):
        user_data = {
            "username": f"user{i}",
            "password": hash_password("password123"),
            "name": f"User {i}",
            "role": random.choice(user_roles),
            "activity_log": [{"action": "Created account", "timestamp": datetime.datetime.now()}]
        }
        users_collection.insert_one(user_data)
    print("20 users inserted successfully!")

def create_items():
    categories = ['Rings', 'Necklaces', 'Bracelets', 'Watches']
    for i in range(1, 201):
        item_data = {
            "product_name": f"Item {i}",
            "sku": 100000 + i,
            "category": random.choice(categories),
            "grams": round(random.uniform(1, 50), 2),
            "ctw_diamond": round(random.uniform(0.1, 5.0), 2),
            "number_of_pcs": random.randint(1, 100),
            "reference_cost": round(random.uniform(50, 5000), 2),
            "our_cost": round(random.uniform(40, 4500), 2),
            "image_path": None
        }
        items_collection.insert_one(item_data)
    print("200 items inserted successfully!")

if __name__ == "__main__":
    create_users()
    create_items()
