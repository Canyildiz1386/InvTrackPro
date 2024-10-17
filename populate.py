from pymongo import MongoClient
import hashlib
import random
import datetime

client = MongoClient('mongodb://localhost:27017/')
db = client['inventory_db']
items_collection = db['items']
users_collection = db['users']
customers_collection = db['customers']
transactions_collection = db['transactions']

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

def create_customers():
    for i in range(1, 51):
        customer_data = {
            "name": f"Customer {i}",
            "contact": f"+1-800-{random.randint(1000000, 9999999)}",
            "address": f"Address {i}, City {random.randint(1, 100)}, Country",
            "email": f"customer{i}@example.com"
        }
        customers_collection.insert_one(customer_data)
    print("50 customers inserted successfully!")

def create_transactions():
    for i in range(1, 101):
        transaction_data = {
            "item_sku": random.randint(100001, 100200),
            "item_name": f"Item {random.randint(1, 200)}",
            "quantity_sold": random.randint(1, 10),
            "unit_price": round(random.uniform(40, 4500), 2),
            "total_cost": round(random.uniform(100, 45000), 2),
            "date": datetime.datetime.now(),
            "customer_name": f"Customer {random.randint(1, 50)}"
        }
        transactions_collection.insert_one(transaction_data)
    print("100 transactions inserted successfully!")

if __name__ == "__main__":
    create_users()
    create_items()
    create_customers()
    create_transactions()
