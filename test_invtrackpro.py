import pytest
from pymongo import MongoClient
import hashlib
import datetime

client = MongoClient('mongodb://localhost:27017/')
db = client['test_inventory_db']
users_collection = db['users']
items_collection = db['items']
customers_collection = db['customers']
transactions_collection = db['transactions']

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
    assert inserted_user["name"] == "Test User"
    assert inserted_user["role"] == "user"
    assert "activity_log" in inserted_user
    assert inserted_user["activity_log"][0]["action"] == "Created account"

def test_create_user_duplicate():
    user_data = {
        "username": "duplicate_user",
        "password": hash_password("password123"),
        "name": "Duplicate User",
        "role": "admin"
    }
    users_collection.insert_one(user_data)
    with pytest.raises(Exception): 
        users_collection.insert_one(user_data)

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
    assert inserted_item["sku"] == 123456
    assert inserted_item["category"] == "Rings"
    assert inserted_item["grams"] == 10.5
    assert inserted_item["ctw_diamond"] == 1.5
    assert inserted_item["number_of_pcs"] == 10

def test_item_stock_deduction():
    item_data = {
        "product_name": "Stock Test Item",
        "sku": 654321,
        "category": "Necklaces",
        "grams": 15.2,
        "ctw_diamond": 2.5,
        "number_of_pcs": 50,
        "reference_cost": 800.0,
        "our_cost": 750.0,
        "image_path": None
    }
    items_collection.insert_one(item_data)
    items_collection.update_one({"sku": 654321}, {"$inc": {"number_of_pcs": -5}})
    
    updated_item = items_collection.find_one({"sku": 654321})
    assert updated_item["number_of_pcs"] == 45

def test_create_customer():
    customer_data = {
        "name": "Test Customer",
        "contact": "+123456789",
        "address": "Test Address",
        "email": "testcustomer@example.com",
        "purchase_history": []
    }
    customers_collection.insert_one(customer_data)
    
    inserted_customer = customers_collection.find_one({"name": "Test Customer"})
    
    assert inserted_customer["name"] == "Test Customer"
    assert inserted_customer["contact"] == "+123456789"
    assert inserted_customer["email"] == "testcustomer@example.com"
    assert isinstance(inserted_customer["purchase_history"], list)

def test_create_transaction():
    item_data = {
        "product_name": "Transaction Test Item",
        "sku": 789101,
        "category": "Bracelets",
        "grams": 12.3,
        "ctw_diamond": 1.8,
        "number_of_pcs": 30,
        "reference_cost": 900.0,
        "our_cost": 850.0,
        "image_path": None
    }
    items_collection.insert_one(item_data)

    customer_data = {
        "name": "Transaction Customer",
        "contact": "+987654321",
        "address": "Customer Address",
        "email": "transactioncustomer@example.com",
        "purchase_history": []
    }
    customers_collection.insert_one(customer_data)
    
    inserted_customer = customers_collection.find_one({"name": "Transaction Customer"})
    
    transaction_data = {
        "customer_id": inserted_customer["_id"],
        "item_sku": 789101,
        "quantity_sold": 5,
        "unit_price": 850.0,
        "total_cost": 4250.0,
        "date": datetime.datetime.now(),
    }
    transactions_collection.insert_one(transaction_data)
    
    inserted_transaction = transactions_collection.find_one({"item_sku": 789101})
    
    assert inserted_transaction["quantity_sold"] == 5
    assert inserted_transaction["total_cost"] == 4250.0

    items_collection.update_one({"sku": 789101}, {"$inc": {"number_of_pcs": -5}})
    updated_item = items_collection.find_one({"sku": 789101})
    assert updated_item["number_of_pcs"] == 25

def teardown_module(module):
    users_collection.delete_many({})
    items_collection.delete_many({})
    customers_collection.delete_many({})
    transactions_collection.delete_many({})
