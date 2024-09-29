
# 📦 InvTrackPro

**InvTrackPro** is a comprehensive inventory management system designed to help businesses manage their stock of items, track user activities, and efficiently log information on products like jewelry items (Rings, Necklaces, Bracelets, and Watches). It uses MongoDB as the database, and supports user roles such as admins and regular users.

## 🌟 Features

- 🔑 **User Management**: Supports both admin and regular user roles.
- 💍 **Item Tracking**: Items are categorized (Rings, Necklaces, Bracelets, Watches) and stored with detailed attributes such as weight, diamond carat, and cost.
- 📊 **Cost Analysis**: Keeps track of reference and actual costs of products.
- 📝 **Activity Logs**: Logs user actions, including account creation and modifications.
- 🔍 **Data Search**: Enables efficient searching and filtering through inventory items.
- 🛠️ **Customizable Fields**: Supports adjustable fields like SKU, product name, and item images.

## 📂 Project Structure

- **`inventory_db`**: MongoDB database to store user and item data.
- **`items_collection`**: Collection where item details such as product name, SKU, weight, cost, etc., are stored.
- **`users_collection`**: Collection for user data, including username, hashed password, and activity logs.

## 🚀 How to Get Started

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Canyildiz1386/InvTrackPro.git
   cd InvTrackPro
   ```

2. **Install the required dependencies**:
   Create a virtual environment and install the necessary packages:
   ```bash
   python3 -m venv env
   source env/bin/activate
   pip install -r requirements.txt
   ```

3. **Set up MongoDB**:
   Make sure you have MongoDB installed and running locally or on a server. Update the connection string in the code if necessary:
   ```python
   client = MongoClient('mongodb://localhost:27017/')
   ```

4. **Run the script** to generate sample users and inventory items:
   ```bash
   python main.py
   ```

   This will insert 20 users and 200 sample inventory items into the database.

## 🧪 Running Tests

Tests are provided to ensure the functionality of the key features of the system.

To run tests:
1. **Install `pytest`** if you don't have it already:
   ```bash
   pip install pytest
   ```

2. **Run the tests**:
   ```bash
   pytest test_invtrackpro.py
   ```

## 🧑‍💻 API and Code Snippets

### User Data Example:
```json
{
  "username": "user1",
  "password": "hashed_password",
  "name": "User 1",
  "role": "admin",
  "activity_log": [
    {
      "action": "Created account",
      "timestamp": "2024-09-29T12:34:56"
    }
  ]
}
```

### Item Data Example:
```json
{
  "product_name": "Item 1",
  "sku": 100001,
  "category": "Rings",
  "grams": 12.5,
  "ctw_diamond": 2.3,
  "number_of_pcs": 45,
  "reference_cost": 230.50,
  "our_cost": 200.75,
  "image_path": null
}
```

## 🛠️ How to Contribute

We welcome contributions! Here's how you can help:

1. Fork the repo and create your branch from `main`.
2. Commit changes to your branch and create a pull request.
3. Ensure all tests pass before requesting reviews.

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 📧 Contact

For any inquiries, feel free to reach out:
- GitHub: [Canyildiz1386](https://github.com/Canyildiz1386)
- Email: can.yildiz.1386@gmail.com

