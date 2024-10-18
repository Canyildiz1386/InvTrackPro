
# 📦 InvTrackPro

### **InvTrackPro** is a comprehensive inventory management system designed to streamline product tracking, manage users, and log sales transactions. Whether you're running a jewelry store or any other business with complex inventory needs, InvTrackPro has got you covered!


## 🌟 Features

- 🛠 **Item Management**: Easily add, edit, and delete items like Rings, Necklaces, Bracelets, and Watches.
- 👤 **User Management**: Admins can create, manage, and assign roles to users (Admin and Regular User).
- 👥 **Customer Management**: Store customer details and purchase history.
- 💼 **Transaction Logging**: Track sales and generate invoices automatically.
- 🔍 **Search Functionality**: Quickly find items, users, customers, and transactions with live search.
- 💾 **Data Backup**: Export your data in JSON or CSV formats to ensure it’s always safe.
- 📊 **Dashboard & Reports**: View summaries, generate reports, and visualize stock levels with charts.
- 📄 **Invoice Generation**: Automatically generate invoices for sales.
- 🔑 **Secure Authentication**: Hash-based password storage ensures user data is safe.
- 📋 **Activity Logging**: Track user actions for accountability and auditing.
- 🔄 **Real-time Stock Updates**: Keep inventory up-to-date with real-time stock deduction after sales.

---

## 🚀 Quick Start

Follow these steps to set up **InvTrackPro** locally on your machine.

### 📦 Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Canyildiz1386/InvTrackPro.git
   cd invtrackpro
   ```

2. **Install the required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up MongoDB**:
   - Make sure MongoDB is running on your local machine. InvTrackPro uses the default MongoDB URI (`mongodb://localhost:27017/`).
   - If you want to change the URI, update the MongoDB connection string in `main.py` and `populate.py`.

4. **Populate the database**:
   ```bash
   python populate.py
   ```
   This script will populate your database with:
   - 20 users 👤
   - 200 items 💍
   - 50 customers 👥
   - 100 transactions 💼

5. **Run the Application**:
   ```bash
   python main.py
   ```

6. **Access the Inventory System**:
   Once running, log in using one of the default users created by the population script:
   - Username: `user1`
   - Password: `password123`
   
   Or register a new account!

---

## 🔧 Running Tests

We have included a set of tests to ensure the smooth functioning of critical features.

1. **Run Tests**:
   ```bash
   pytest test_invtrackpro.py
   ```

   Tests cover:
   - 🧪 User creation
   - 🧪 Item stock management
   - 🧪 Customer management
   - 🧪 Transactions logging and validation

---

## 🛠 Features Breakdown

### 📦 Inventory Management

- **Add New Items**: Enter details such as item name, SKU, category, weight, cost, and image.
- **Update Stock**: Track and update the number of items in stock in real-time.
- **View Inventory**: Visualize your entire stock with filtering options by category, SKU, and name.

### 💼 Transactions & Invoices

- **Sell Items**: Record item sales by selecting from available customers and entering sold quantities.
- **Generate Invoices**: Automatically generate and save invoices after each sale.
- **View Transactions**: Easily search and review past transactions.

### 👥 User Management

- **Admin and User Roles**: Admins have full access to manage items, users, and view reports. Regular users can access items and transactions.
- **Activity Logs**: Each user’s actions are logged for transparency and accountability.

### 👤 Customer Management

- **Store Customer Information**: Keep records of customer contact info, purchase history, and address.
- **Customer Search**: Quickly search for customers by name or contact number.

### 📊 Dashboard & Reports

- **Stock Summary**: View a summary of items, including total stock, total value, and low-stock alerts.
- **Pie Chart Visualization**: View stock distribution by item categories.
- **Generate Reports**: Export detailed reports in JSON or CSV format, including inventory, users, transactions, and customer data.

---

## 🔐 Security

- **Password Hashing**: User passwords are securely hashed using SHA-256 for safe storage.
- **User Roles**: Different user permissions ensure that sensitive actions are only performed by authorized personnel.

---

## 💻 Technologies Used

- **Frontend**: CustomTkinter for a sleek, modern GUI.
- **Backend**: Python with MongoDB for data storage.
- **Visualization**: Matplotlib for charts and data visualizations.
- **Libraries**: 
   - `pymongo` for database interactions.
   - `Pillow` for image handling.
   - `qrcode` for QR code generation.
   - `matplotlib` for data visualization.
   - `pytest` for testing.

---

## 📄 Future Enhancements

- 🔔 **Email Notifications**: Notify customers with email receipts after a transaction.
- 🛒 **Shopping Cart**: Add functionality for customers to order multiple items at once.
- 📱 **Mobile Support**: Build a responsive mobile version for easy stock management on the go.
- 📊 **Advanced Analytics**: Add more detailed sales analytics with graphs and trend lines.

---

## 🏆 Contributions

We welcome contributions! Feel free to fork this repo, submit issues, or create pull requests. 🎉

---

## 👨‍💻 Author

- **Can yildiz** - [Your GitHub](https://github.com/Canyildiz1386)

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---