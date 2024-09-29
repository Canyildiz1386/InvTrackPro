import pytest
from pymongo import MongoClient
import hashlib
import datetime

client = MongoClient('mongodb://localhost:27017/')
db = client['test_inventory_db']
users_collection = db['users']
items_collection = db['items']

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def test_create_user():
    user_data = {
        "username": "test_user",
        "password": hash_password("password123"),
        "name": "Test User",
        "role": "user",
        "activity_log": [{"action": "Created account", "timestamp": datetime.datetime.now()}]
    }
    users_collection.insert_one(user_data)
    
    inserted_user = users_collection.find_one({"username": "test_user"})
    
    assert inserted_user["username"] == "test_user"
    assert inserted_user["password"] == hash_password("password123")

def test_create_item():
    item_data = {
        "product_name": "Test Item",
        "sku": 123456,
        "category": "Rings",
        "grams": 10.5,
        "ctw_diamond": 1.5,
        "number_of_pcs": 10,
        "reference_cost": 500.0,
        "our_cost": 450.0,
        "image_path": None
    }
    items_collection.insert_one(item_data)
    
    inserted_item = items_collection.find_one({"sku": 123456})
    
    assert inserted_item["product_name"] == "Test Item"
    assert inserted_item["grams"] == 10.5
    assert inserted_item["ctw_diamond"] == 1.5

def teardown_module(module):
    users_collection.delete_many({})
    items_collection.delete_many({})
