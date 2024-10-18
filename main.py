import customtkinter as ctk
from tkinter import filedialog, ttk, messagebox
from PIL import Image, ImageTk
import os
from pymongo import MongoClient
import hashlib
import datetime
import tkinter as tk
from tkinter import Menu
import qrcode
from customtkinter import CTkImage
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json
import csv

client = MongoClient('mongodb://localhost:27017/')
db = client['inventory_db']
items_collection = db['items']
users_collection = db['users']
customers_collection = db['customers']  # New collection for customers
transactions_collection = db['transactions']  # New collection for sales transactions

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("🔐 Inventory Management System 🔐")
        self.geometry("1080x720")
        
        self.configure(bg="#1A1A1D")
        self.image_path = None
        self.sku_counter = self.get_next_sku()
        self.inventory = list(items_collection.find())
        self.inventory_frame = None
        self.tree = None
        self.total_pieces_label = None
        self.total_cost_label = None
        self.current_user = None
        self.show_login_screen()

    def get_next_sku(self):
        last_item = items_collection.find_one(sort=[("sku", -1)])
        return last_item['sku'] + 1 if last_item else 100001

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def register_user(self, username, password, name, role='user'):
        if users_collection.find_one({"username": username}):
            messagebox.showerror("❌ Error ❌", "Username already exists!")
            return False
        hashed_password = self.hash_password(password)
        users_collection.insert_one({
            "username": username,
            "password": hashed_password,
            "name": name,
            "role": role  # Save the role (user or admin)
        })
        messagebox.showinfo("✅ Success ✅", "Registration successful!")
        self.show_login_screen()


    def authenticate_user(self, username, password):
        hashed_password = self.hash_password(password)
        user = users_collection.find_one({"username": username, "password": hashed_password})
        if user:
            self.current_user = user
            return True
        return False

    def log_activity(self, action):
        users_collection.update_one(
            {"username": self.current_user["username"]},
            {"$push": {"activity_log": {"action": action, "timestamp": datetime.datetime.now()}}}
        )

    def show_login_screen(self):
        self.clear_widgets()

        header = ctk.CTkLabel(self, text="🔑 Login 🔑", font=("Arial", 36, "bold"), text_color="white")
        header.pack(pady=20)
        username_entry = ctk.CTkEntry(self, placeholder_text="👤 Username 👤", width=300)
        username_entry.pack(pady=10)
        password_entry = ctk.CTkEntry(self, placeholder_text="🔒 Password 🔒", show="*", width=300)
        password_entry.pack(pady=10)

        def login():
            username = username_entry.get()
            password = password_entry.get()
            if self.authenticate_user(username, password):
                messagebox.showinfo("✅ Success ✅", "Login successful!")
                self.setup_home_screen()
            else:
                messagebox.showerror("❌ Error ❌", "Invalid username or password.")

        login_btn = ctk.CTkButton(self, text="🔓 Login 🔓", corner_radius=10, command=login, width=200, height=40)
        login_btn.pack(pady=10)


    def backup_data(self):
        backup_window = ctk.CTkToplevel(self)
        backup_window.title("🔄 Backup Data 🔄")
        backup_window.geometry("400x200")

        ctk.CTkLabel(backup_window, text="📂 Choose Backup Format 📂", font=("Arial", 16, "bold")).pack(pady=20)

        json_btn = ctk.CTkButton(backup_window, text="📄 Backup to JSON 📄", corner_radius=10, command=self.backup_to_json, width=200, height=40)
        json_btn.pack(pady=10)

        csv_btn = ctk.CTkButton(backup_window, text="📄 Backup to CSV 📄", corner_radius=10, command=self.backup_to_csv, width=200, height=40)
        csv_btn.pack(pady=10)

    def backup_to_json(self):
        data = {
            "items": list(items_collection.find()),
            "users": list(users_collection.find()),
            "customers": list(customers_collection.find()),  # Backup customer data
            "transactions": list(transactions_collection.find())  # Backup transactions data
        }
        backup_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if backup_path:
            with open(backup_path, 'w') as file:
                json.dump(data, file, default=str)
            messagebox.showinfo("✅ Success ✅", "Data backed up to JSON file successfully!")

    def backup_to_csv(self):
        data = {
            "items": list(items_collection.find()),
            "users": list(users_collection.find()),
            "customers": list(customers_collection.find()),  # Include customer data
            "transactions": list(transactions_collection.find())  # Include transaction data
        }
        backup_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if backup_path:
            with open(backup_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Items"])
                writer.writerow(data["items"][0].keys())
                for item in data["items"]:
                    writer.writerow(item.values())
                writer.writerow(["Users"])
                writer.writerow(data["users"][0].keys())
                for user in data["users"]:
                    writer.writerow(user.values())
                writer.writerow(["Customers"])
                writer.writerow(data["customers"][0].keys())
                for customer in data["customers"]:
                    writer.writerow(customer.values())
                writer.writerow(["Transactions"])
                writer.writerow(data["transactions"][0].keys())
                for transaction in data["transactions"]:
                    writer.writerow(transaction.values())
            messagebox.showinfo("✅ Success ✅", "Data backed up to CSV file successfully!")

    def generate_report(self):
        report_window = ctk.CTkToplevel(self)
        report_window.title("📊 Generate Inventory & User Report 📊")
        report_window.geometry("400x200")

        ctk.CTkLabel(report_window, text="📄 Choose Report Format 📄", font=("Arial", 16, "bold")).pack(pady=20)

        json_report_btn = ctk.CTkButton(report_window, text="📄 Generate JSON Report 📄", corner_radius=10, command=self.report_to_json, width=200, height=40)
        json_report_btn.pack(pady=10)

        csv_report_btn = ctk.CTkButton(report_window, text="📄 Generate CSV Report 📄", corner_radius=10, command=self.report_to_csv, width=200, height=40)
        csv_report_btn.pack(pady=10)

    def report_to_json(self):
        total_pieces = sum(item['number_of_pcs'] for item in self.inventory)
        total_cost = sum(item['our_cost'] * item['number_of_pcs'] for item in self.inventory)
        report_data = {
            "Inventory Summary": [{"Item": item['product_name'], "SKU": item['sku'], "Category": item['category'], "Stock": item['number_of_pcs'], "Cost": item['our_cost']} for item in self.inventory],
            "User Activities": list(users_collection.find({}, {"username": 1, "activity_log": 1})),
            "Sales Transactions": list(transactions_collection.find()),  # Include sales transaction data
            "Customers": list(customers_collection.find())  # Include customer data
        }
        report_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if report_path:
            with open(report_path, 'w') as file:
                json.dump(report_data, file, default=str)
            messagebox.showinfo("✅ Success ✅", "Inventory and User report generated in JSON format!")

    def report_to_csv(self):
        report_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if report_path:
            with open(report_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Inventory Summary"])
                writer.writerow(["Item", "SKU", "Category", "Stock", "Cost"])
                for item in self.inventory:
                    writer.writerow([item['product_name'], item['sku'], item['category'], item['number_of_pcs'], item['our_cost']])
                writer.writerow(["User Activities"])
                users = users_collection.find({}, {"username": 1, "activity_log": 1})
                for user in users:
                    writer.writerow([f"User: {user['username']}"])
                    for log in user["activity_log"]:
                        writer.writerow([f"Action: {log['action']}, Timestamp: {log['timestamp']}"])
                writer.writerow(["Sales Transactions"])
                transactions = transactions_collection.find()
                for transaction in transactions:
                    writer.writerow([f"Transaction ID: {transaction['_id']}, Date: {transaction['date']}, Total: {transaction['total_cost']}"])
                writer.writerow(["Customers"])
                for customer in customers_collection.find():
                    writer.writerow([f"Customer Name: {customer['name']}, Contact: {customer['contact']}"])
            messagebox.showinfo("✅ Success ✅", "Inventory and User report generated in CSV format!")

    def show_register_screen(self):
        self.clear_widgets()

        header = ctk.CTkLabel(self, text="📝 Register 📝", font=("Arial", 36, "bold"), text_color="white")
        header.pack(pady=20)
        name_entry = ctk.CTkEntry(self, placeholder_text="👤 Name 👤", width=300)
        name_entry.pack(pady=10)
        username_entry = ctk.CTkEntry(self, placeholder_text="👤 Username 👤", width=300)
        username_entry.pack(pady=10)
        password_entry = ctk.CTkEntry(self, placeholder_text="🔑 Password 🔑", show="*", width=300)
        password_entry.pack(pady=10)

        def register():
            name = name_entry.get()
            username = username_entry.get()
            password = password_entry.get()
            if len(password) < 6:
                messagebox.showerror("❌ Error ❌", "Password must be at least 6 characters long.")
                return
            if username and password and name:
                self.register_user(username, password, name)
            else:
                messagebox.showerror("❌ Error ❌", "All fields are required.")

        register_btn = ctk.CTkButton(self, text="📝 Register 📝", corner_radius=10, command=register, width=200, height=40)
        register_btn.pack(pady=10)
        back_btn = ctk.CTkButton(self, text="🔙 Back to Login 🔙", corner_radius=10, command=self.show_login_screen, width=200, height=40)
        back_btn.pack(pady=10)

    def setup_home_screen(self):
        self.clear_widgets()

        username = self.current_user.get('name', 'User')  
        hello_label = ctk.CTkLabel(self, text=f"👋 Hello, {username}! Welcome to the Inventory System", font=("Arial", 36, "bold"), text_color="white")
        hello_label.pack(pady=20)

        self.inventory = list(items_collection.find())

        header = ctk.CTkLabel(self, text="🏠 Inventory System 🏠", font=("Arial", 36, "bold"), text_color="white")
        header.pack(pady=20)

        button_frame = ctk.CTkFrame(self, fg_color="#2C2F33", corner_radius=10)
        button_frame.pack(pady=10, padx=20, fill="x")

        manage_items_btn = ctk.CTkButton(button_frame, text="🛠 Manage Items 🛠", corner_radius=10, command=self.manage_items_screen, width=200, height=40)
        manage_items_btn.grid(row=0, column=0, padx=20, pady=10)

        manage_users_btn = ctk.CTkButton(button_frame, text="👤 Manage Users 👤", corner_radius=10, command=self.manage_users_screen, width=200, height=40)
        manage_users_btn.grid(row=0, column=1, padx=20, pady=10)

        manage_customers_btn = ctk.CTkButton(button_frame, text="👥 Manage Customers 👥", corner_radius=10, command=self.manage_customers_screen, width=200, height=40)
        manage_customers_btn.grid(row=0, column=2, padx=20, pady=10)

        # New "Manage Transactions" button
        manage_transactions_btn = ctk.CTkButton(button_frame, text="💼 Manage Transactions 💼", corner_radius=10, command=self.manage_transactions_screen, width=200, height=40)
        manage_transactions_btn.grid(row=0, column=3, padx=20, pady=10)

        dashboard_btn = ctk.CTkButton(button_frame, text="📊 View Dashboard 📊", corner_radius=10, command=self.setup_dashboard_screen, width=200, height=40)
        dashboard_btn.grid(row=0, column=4, padx=20, pady=10)

        self.inventory_frame = ctk.CTkFrame(self, fg_color="#2C2F33", corner_radius=10)
        self.inventory_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.create_inventory_overview()

    def search_transactions(self, *args):
        search_query = self.search_entry.get()
        query = {}
        if search_query:
            query["$or"] = [
                {"item_name": {"$regex": search_query, "$options": "i"}},
                {"date": {"$regex": search_query, "$options": "i"}}
            ]
        transactions = list(transactions_collection.find(query))
        for widget in self.transactions_frame.winfo_children():
            widget.destroy()
        self.show_transactions_table(self.transactions_frame, transactions)

    def show_transactions_table(self, parent, transactions=None):
        if transactions is None:
            transactions = list(transactions_collection.find())

        tree_scroll = ttk.Scrollbar(parent)
        tree_scroll.pack(side="right", fill="y")

        # Add Transaction ID and Customer Name columns
        self.transactions_tree = ttk.Treeview(parent, columns=("Transaction ID", "Customer Name", "Item", "SKU", "Quantity Sold", "Total Cost", "Date"), show="headings", yscrollcommand=tree_scroll.set)
        
        # Set up headings
        self.transactions_tree.heading("Transaction ID", text="🆔 Transaction ID 🆔")
        self.transactions_tree.heading("Customer Name", text="👤 Customer Name 👤")
        self.transactions_tree.heading("Item", text="🛍️ Item 🛍️")
        self.transactions_tree.heading("SKU", text="📦 SKU 📦")
        self.transactions_tree.heading("Quantity Sold", text="🔢 Quantity Sold 🔢")
        self.transactions_tree.heading("Total Cost", text="💰 Total Cost 💰")
        self.transactions_tree.heading("Date", text="📅 Date 📅")

        self.transactions_tree.pack(fill="both", expand=True, padx=20, pady=10)
        tree_scroll.config(command=self.transactions_tree.yview)

        # Insert data into the treeview
        for transaction in transactions:
            self.transactions_tree.insert("", "end", values=(
                str(transaction.get("_id", "")),  # Convert ObjectId to string for display
                transaction.get("customer_name", ""),  # Customer Name
                transaction.get("item_name", ""),
                transaction.get("item_sku", ""),
                transaction.get("quantity_sold", ""),
                f"${transaction.get('total_cost', 0):.2f}",
                transaction.get("date", "")
            ))

        # Bind to show context menu for transactions
        self.transactions_tree.bind("<Double-1>", self.show_transaction_context_menu)

    def show_transaction_context_menu(self, event):
        menu = Menu(self, tearoff=0)

        item = self.transactions_tree.identify_row(event.y)
        if item:
            self.transactions_tree.selection_set(item)
            selected_transaction = self.transactions_tree.item(item, "values")
            transaction_id = selected_transaction[0]  # Transaction ID is now the first column
            transaction = transactions_collection.find_one({"_id": ObjectId(transaction_id)})

            # Add options to the context menu
            menu.add_command(label="❌ Delete Transaction ❌", command=lambda: self.delete_transaction(transaction))

            menu.post(event.x_root, event.y_root)

    def delete_transaction(self, transaction):
        confirm = messagebox.askyesno("🗑️ Confirm Delete 🗑️", f"Are you sure you want to delete this transaction?")
        if confirm:
            transactions_collection.delete_one({"_id": transaction["_id"]})
            messagebox.showinfo("🗑️ Deleted 🗑️", f"Transaction deleted!")
            self.manage_transactions_screen()


    def manage_transactions_screen(self):
        self.clear_widgets()

        header = ctk.CTkLabel(self, text="💼 Manage Transactions 💼", font=("Arial", 36, "bold"), text_color="white")
        header.pack(pady=20)

        search_frame = ctk.CTkFrame(self, fg_color="#2C2F33", corner_radius=10)
        search_frame.pack(pady=10, padx=20, fill="x")

        search_entry = ctk.CTkEntry(search_frame, placeholder_text="🔍 Search by Item Name or Date 🔍", width=400)
        search_entry.grid(row=0, column=0, padx=10, pady=10)
        search_entry.bind("<KeyRelease>", self.search_transactions)

        self.search_entry = search_entry

        self.transactions_frame = ctk.CTkFrame(self, fg_color="#2C2F33", corner_radius=10)
        self.transactions_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Button for creating a new invoice
        create_invoice_btn = ctk.CTkButton(self, text="📝 Create Invoice 📝", corner_radius=10, command=self.create_invoice_screen, width=200)
        create_invoice_btn.pack(pady=10)

        self.show_transactions_table(self.transactions_frame)

        back_btn = ctk.CTkButton(self, text="🔙 Back to Home 🔙", corner_radius=10, command=self.setup_home_screen, width=200, height=40)
        back_btn.pack(pady=10)
    def create_invoice_screen(self):
        self.clear_widgets()

        header = ctk.CTkLabel(self, text="📝 Create New Invoice 📝", font=("Arial", 36, "bold"), text_color="white")
        header.pack(pady=20)

        # Dropdown for selecting customer from the list
        customer_label = ctk.CTkLabel(self, text="👤 Select Customer 👤", font=("Arial", 16), text_color="white")
        customer_label.pack(pady=10)

        customer_list = [customer['name'] for customer in customers_collection.find()]
        customer_selection = ctk.CTkComboBox(self, values=customer_list, width=300)
        customer_selection.pack(pady=10)

        # Dropdown for selecting items (can be enhanced to allow multiple item selection)
        item_label = ctk.CTkLabel(self, text="🛍️ Select Item 🛍️", font=("Arial", 16), text_color="white")
        item_label.pack(pady=10)

        item_list = [item['product_name'] for item in items_collection.find()]
        item_selection = ctk.CTkComboBox(self, values=item_list, width=300)
        item_selection.pack(pady=10)

        quantity_label = ctk.CTkLabel(self, text="🔢 Enter Quantity 🔢", font=("Arial", 16), text_color="white")
        quantity_label.pack(pady=10)
        quantity_entry = ctk.CTkEntry(self, width=300)
        quantity_entry.pack(pady=10)

        def confirm_transaction():
            customer_name = customer_selection.get()
            item_name = item_selection.get()
            quantity = int(quantity_entry.get())

            if not customer_name or not item_name or not quantity:
                messagebox.showerror("❌ Error ❌", "Please select a customer, item, and quantity.")
                return

            # Fetch the selected item and customer from the database
            item = items_collection.find_one({"product_name": item_name})
            customer = customers_collection.find_one({"name": customer_name})

            if item and customer:
                if quantity > item['number_of_pcs']:
                    messagebox.showerror("❌ Error ❌", "Insufficient stock.")
                    return

                # Deduct the quantity from the stock
                new_stock = item['number_of_pcs'] - quantity
                items_collection.update_one({"_id": item['_id']}, {"$set": {"number_of_pcs": new_stock}})

                # Record the transaction in the transactions collection
                transaction = {
                    "customer_name": customer_name,
                    "item_sku": item['sku'],
                    "item_name": item_name,
                    "quantity_sold": quantity,
                    "unit_price": item['our_cost'],
                    "total_cost": item['our_cost'] * quantity,
                    "date": datetime.datetime.now()
                }
                transactions_collection.insert_one(transaction)

                # Generate the invoice
                self.generate_invoice(customer_name, item, quantity)
                messagebox.showinfo("✅ Success ✅", "Transaction completed and invoice generated.")
                self.manage_transactions_screen()
            else:
                messagebox.showerror("❌ Error ❌", "Invalid customer or item selection.")

        # Confirm transaction button
        confirm_btn = ctk.CTkButton(self, text="✔ Confirm Transaction ✔", corner_radius=10, command=confirm_transaction, width=200, height=40)
        confirm_btn.pack(pady=10)

        back_btn = ctk.CTkButton(self, text="🔙 Back to Transactions 🔙", corner_radius=10, command=self.manage_transactions_screen, width=200, height=40)
        back_btn.pack(pady=10)

    def generate_invoice(self, customer_name, item, quantity_sold):
        invoice_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        total_cost = item['our_cost'] * quantity_sold

        invoice_content = f"""
        Inventory Management System
        ==========================
        
        Invoice for Sale
        Date: {invoice_date}

        Customer: {customer_name}
        
        Sold Item:
        ----------
        Product Name: {item['product_name']}
        SKU: {item['sku']}
        Category: {item['category']}
        Quantity Sold: {quantity_sold}
        Unit Price: ${item['our_cost']:.2f}
        Total Cost: ${total_cost:.2f}
        
        Thank you for your purchase!
        ==========================
        """

        save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if save_path:
            if save_path.endswith('.txt'):
                with open(save_path, 'w') as file:
                    file.write(invoice_content)
                messagebox.showinfo("✅ Success ✅", "Invoice generated successfully!")

    def manage_items_screen(self):
        self.clear_widgets()

        header = ctk.CTkLabel(self, text="🛠 Manage Items 🛠", font=("Arial", 36, "bold"), text_color="white")
        header.pack(pady=20)

        add_item_btn = ctk.CTkButton(self, text="➕ Add New Item ➕", corner_radius=10, command=self.add_item_screen, width=200, height=40)
        add_item_btn.pack(pady=10)
        
        add_quantity_btn = ctk.CTkButton(self, text="📦 Add Quantity 📦", corner_radius=10, command=self.add_quantity_screen, width=200, height=40)
        add_quantity_btn.pack(pady=10)

        back_btn = ctk.CTkButton(self, text="🔙 Back to Home 🔙", corner_radius=10, command=self.setup_home_screen, width=200, height=40)
        back_btn.pack(pady=10)

    def setup_dashboard_screen(self):
        self.clear_widgets()

        header = ctk.CTkLabel(self, text="📊 Inventory Dashboard 📊", font=("Arial", 36, "bold"), text_color="white")
        header.pack(pady=20)

        button_frame = ctk.CTkFrame(self, fg_color="#2C2F33", corner_radius=10)
        button_frame.pack(pady=10, padx=20, fill="x")

        back_btn = ctk.CTkButton(button_frame, text="🔙 Back to Home 🔙", corner_radius=10, command=self.setup_home_screen, width=200, height=40)
        back_btn.grid(row=0, column=0, padx=20, pady=10)

        if self.current_user['role'] == 'admin':
            backup_btn = ctk.CTkButton(button_frame, text="🔄 Backup Data 🔄", corner_radius=10, command=self.backup_data, width=200, height=40)
            backup_btn.grid(row=0, column=1, padx=20, pady=10)

            report_btn = ctk.CTkButton(button_frame, text="📄 Generate Report 📄", corner_radius=10, command=self.generate_report, width=200, height=40)
            report_btn.grid(row=0, column=2, padx=20, pady=10)

        self.create_summary_widget()
        self.create_charts()

    def create_summary_widget(self):
        most_expensive_item = max(self.inventory, key=lambda x: x['our_cost'])['product_name']
        least_stock_item = min(self.inventory, key=lambda x: x['number_of_pcs'])['product_name']

        summary_frame = ctk.CTkFrame(self, fg_color="#2C2F33", corner_radius=10)
        summary_frame.pack(pady=10, padx=20, fill="x")

        most_expensive_label = ctk.CTkLabel(summary_frame, text=f"💰 Most Expensive Item 💰: {most_expensive_item}", text_color="white", font=("Arial", 18))
        most_expensive_label.grid(row=0, column=0, padx=20, pady=10)

        least_stock_label = ctk.CTkLabel(summary_frame, text=f"📦 Item with Least Stock 📦: {least_stock_item}", text_color="white", font=("Arial", 18))
        least_stock_label.grid(row=0, column=1, padx=20, pady=10)

    def create_charts(self):
        chart_frame = ctk.CTkFrame(self, fg_color="#2C2F33", corner_radius=10)
        chart_frame.pack(pady=20, padx=20, fill="both", expand=True)

        categories = [item['category'] for item in self.inventory]
        category_count = {cat: categories.count(cat) for cat in set(categories)}
        labels = category_count.keys()
        sizes = category_count.values()

        fig, ax = plt.subplots(figsize=(6, 6))
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')

        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side="left", fill="both", expand=True)

        fig2, ax2 = plt.subplots(figsize=(6, 6))
        ax2.bar(category_count.keys(), category_count.values())
        ax2.set_title('📊 Stock Levels by Category 📊')
        ax2.set_xlabel('🏷️ Category 🏷️')
        ax2.set_ylabel('📦 Number of Items 📦')

        canvas2 = FigureCanvasTkAgg(fig2, master=chart_frame)
        canvas2.draw()
        canvas2.get_tk_widget().pack(side="right", fill="both", expand=True)

    def live_search(self, *args):
        search_query = self.search_entry.get()
        category = self.filter_category.get()
        query = {}
        if search_query:
            if search_query.isdigit():
                query["sku"] = int(search_query)
            else:
                query["product_name"] = {"$regex": search_query, "$options": "i"}
        if category != "All":
            query["category"] = category
        self.inventory = list(items_collection.find(query))
        self.create_inventory_overview()

    def create_inventory_overview(self):
        total_pieces = sum(item['number_of_pcs'] for item in self.inventory)
        total_cost = sum(item['our_cost'] * item['number_of_pcs'] for item in self.inventory)

        if self.total_pieces_label and self.total_pieces_label.winfo_exists():
            self.total_pieces_label.configure(text=f"📦 Total Pieces 📦: {total_pieces}")
        else:
            self.total_pieces_label = ctk.CTkLabel(
                self.inventory_frame,
                text=f"📦 Total Pieces 📦: {total_pieces}",
                text_color="white",
                font=("Arial", 18)
            )
            self.total_pieces_label.pack(pady=10)

        if self.total_cost_label and self.total_cost_label.winfo_exists():
            self.total_cost_label.configure(text=f"💲 Total Cost 💲: ${total_cost:.2f}")
        else:
            self.total_cost_label = ctk.CTkLabel(
                self.inventory_frame,
                text=f"💲 Total Cost 💲: ${total_cost:.2f}",
                text_color="white",
                font=("Arial", 18)
            )
            self.total_cost_label.pack(pady=10)

        self.show_inventory_table(self.inventory_frame)

    def show_inventory_table(self, parent):
        if hasattr(self, 'tree') and self.tree:
            self.tree.delete(*self.tree.get_children())
        else:
            tree_scroll = ttk.Scrollbar(parent)
            tree_scroll.pack(side="right", fill="y")
            self.tree = ttk.Treeview(parent, columns=("Item", "SKU", "Category", "Cost", "Stock"), show="headings", yscrollcommand=tree_scroll.set)
            self.tree.heading("Item", text="🛍️ Item 🛍️")
            self.tree.heading("SKU", text="📦 SKU 📦")
            self.tree.heading("Category", text="🏷️ Category 🏷️")
            self.tree.heading("Cost", text="💰 Cost 💰")
            self.tree.heading("Stock", text="📊 Stock 📊")
            self.tree.column("Item", anchor="w", width=150)
            self.tree.column("SKU", anchor="center", width=100)
            self.tree.column("Category", anchor="center", width=100)
            self.tree.column("Cost", anchor="center", width=100)
            self.tree.column("Stock", anchor="center", width=100)
            self.tree.pack(fill="both", expand=True, padx=20, pady=10)
            tree_scroll.config(command=self.tree.yview)

            self.tree.bind("<Double-1>", self.show_inventory_context_menu)

        for item in self.inventory:
            self.tree.insert("", "end", values=(
                item.get("product_name", ""),
                item.get("sku", ""),
                item.get("category", ""),
                f"${item.get('our_cost', 0):.2f}",
                item.get("number_of_pcs", 0),
            ))

    def manage_customers_screen(self):
        self.clear_widgets()

        header = ctk.CTkLabel(self, text="👥 Manage Customers 👥", font=("Arial", 36, "bold"), text_color="white")
        header.pack(pady=20)

        search_frame = ctk.CTkFrame(self, fg_color="#2C2F33", corner_radius=10)
        search_frame.pack(pady=10, padx=20, fill="x")

        search_entry = ctk.CTkEntry(search_frame, placeholder_text="🔍 Search by Name/Contact 🔍", width=400)
        search_entry.grid(row=0, column=0, padx=10, pady=10)
        search_entry.bind("<KeyRelease>", self.search_customers)

        add_customer_btn = ctk.CTkButton(search_frame, text="➕ Add Customer ➕", corner_radius=10, command=self.add_customer_screen, width=200)
        add_customer_btn.grid(row=0, column=1, padx=10, pady=10)

        self.search_entry = search_entry

        self.customer_frame = ctk.CTkFrame(self, fg_color="#2C2F33", corner_radius=10)
        self.customer_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.show_customers_table(self.customer_frame)

        back_btn = ctk.CTkButton(self, text="🔙 Back to Home 🔙", corner_radius=10, command=self.setup_home_screen, width=200, height=40)
        back_btn.pack(pady=10)

    def search_customers(self, *args):
        search_query = self.search_entry.get()
        query = {}
        if search_query:
            query["$or"] = [
                {"name": {"$regex": search_query, "$options": "i"}},
                {"contact": {"$regex": search_query, "$options": "i"}},
            ]
        customers = list(customers_collection.find(query))
        for widget in self.customer_frame.winfo_children():
            widget.destroy()
        self.show_customers_table(self.customer_frame, customers)

    def show_customers_table(self, parent, customers=None):
        if customers is None:
            customers = list(customers_collection.find())
        tree_scroll = ttk.Scrollbar(parent)
        tree_scroll.pack(side="right", fill="y")
        self.customer_tree = ttk.Treeview(parent, columns=("Name", "Contact"), show="headings", yscrollcommand=tree_scroll.set)
        self.customer_tree.heading("Name", text="👤 Name 👤")
        self.customer_tree.heading("Contact", text="📞 Contact 📞")
        self.customer_tree.pack(fill="both", expand=True, padx=20, pady=10)
        tree_scroll.config(command=self.customer_tree.yview)

        for customer in customers:
            self.customer_tree.insert("", "end", values=(
                customer['name'],
                customer['contact']
            ))

        self.customer_tree.bind("<Double-1>", self.show_customer_context_menu)

    def show_customer_context_menu(self, event):
        menu = Menu(self, tearoff=0)

        item = self.customer_tree.identify_row(event.y)
        if item:
            self.customer_tree.selection_set(item)
            selected_customer = self.customer_tree.item(item, "values")
            customer = customers_collection.find_one({"name": selected_customer[0]})

            menu.add_command(label="✏ Edit Customer ✏", command=lambda: self.edit_customer_screen(customer))
            menu.add_command(label="❌ Delete Customer ❌", command=lambda: self.delete_customer(customer))

            menu.post(event.x_root, event.y_root)

    def add_customer_screen(self):
        self.clear_widgets()

        header = ctk.CTkLabel(self, text="➕ Add New Customer ➕", font=("Arial", 36, "bold"), text_color="white")
        header.pack(pady=20)

        name_entry = ctk.CTkEntry(self, placeholder_text="👤 Name 👤", width=300)
        name_entry.pack(pady=10)
        contact_entry = ctk.CTkEntry(self, placeholder_text="📞 Contact 📞", width=300)
        contact_entry.pack(pady=10)

        def save_customer():
            customer_data = {
                "name": name_entry.get(),
                "contact": contact_entry.get(),
            }
            customers_collection.insert_one(customer_data)
            messagebox.showinfo("✅ Success ✅", "Customer added successfully!")
            self.manage_customers_screen()

        save_btn = ctk.CTkButton(self, text="💾 Save Customer 💾", corner_radius=10, command=save_customer, width=200, height=40)
        save_btn.pack(pady=10)
        back_btn = ctk.CTkButton(self, text="🔙 Back to Manage Customers 🔙", corner_radius=10, command=self.manage_customers_screen, width=200, height=40)
        back_btn.pack(pady=10)

    def edit_customer_screen(self, customer):
        self.clear_widgets()

        header = ctk.CTkLabel(self, text="✏ Edit Customer ✏", font=("Arial", 36, "bold"), text_color="white")
        header.pack(pady=20)

        name_entry = ctk.CTkEntry(self, placeholder_text="👤 Name 👤", width=300)
        name_entry.insert(0, customer['name'])
        name_entry.pack(pady=10)
        contact_entry = ctk.CTkEntry(self, placeholder_text="📞 Contact 📞", width=300)
        contact_entry.insert(0, customer['contact'])
        contact_entry.pack(pady=10)

        def save_customer():
            customers_collection.update_one(
                {"_id": customer["_id"]},
                {"$set": {"name": name_entry.get(), "contact": contact_entry.get()}}
            )
            messagebox.showinfo("✅ Success ✅", "Customer updated successfully!")
            self.manage_customers_screen()

        save_btn = ctk.CTkButton(self, text="💾 Save Customer 💾", corner_radius=10, command=save_customer, width=200, height=40)
        save_btn.pack(pady=10)

    def delete_customer(self, customer):
        confirm = messagebox.askyesno("🗑️ Confirm Delete 🗑️", f"Are you sure you want to delete {customer['name']}?")
        if confirm:
            customers_collection.delete_one({"_id": customer["_id"]})
            messagebox.showinfo("🗑️ Deleted 🗑️", f"Customer {customer['name']} deleted!")
            self.manage_customers_screen()


    def add_item_screen(self):
        self.clear_widgets()
        header = ctk.CTkLabel(self, text="➕ Add New Inventory Item ➕", font=("Arial", 30, "bold"), text_color="white")
        header.pack(pady=20)
        self.create_item_form(self.save_new_item)

    def create_item_form(self, save_command, item=None):
        form_frame = ctk.CTkFrame(self, fg_color="#2C2F33", corner_radius=10)
        form_frame.pack(pady=20, padx=20, fill="both", expand=True)
        img_label = ctk.CTkLabel(form_frame, text="🖼️ No Image Uploaded 🖼️", text_color="white", width=200)
        img_label.grid(row=0, column=1, padx=20, pady=10)
        img_btn = ctk.CTkButton(form_frame, text="📤 Upload Image 📤", corner_radius=10, command=lambda: self.upload_image(img_label), width=200)
        img_btn.grid(row=0, column=0, padx=20, pady=10)
        form_fields = [
            ("Item Name", ctk.CTkEntry(form_frame, width=300)),
            ("SKU", ctk.CTkEntry(form_frame, width=300, state='disabled')),
            ("Category", ctk.CTkComboBox(form_frame, width=300, values=["Rings", "Necklaces", "Bracelets", "Watches"])),
            ("Grams", ctk.CTkEntry(form_frame, width=300)),
            ("CTW Diamond", ctk.CTkEntry(form_frame, width=300)),
            ("Number of Pieces", ctk.CTkEntry(form_frame, width=300)),
            ("Reference Cost", ctk.CTkEntry(form_frame, width=300)),
            ("Our Cost", ctk.CTkEntry(form_frame, width=300)),
        ]

        self.form_entries = {}
        for i, (label_text, entry) in enumerate(form_fields):
            ctk.CTkLabel(form_frame, text=label_text, text_color="white", font=("Arial", 14)).grid(row=i + 1, column=0, padx=20, pady=10, sticky="e")
            entry.grid(row=i + 1, column=1, padx=20, pady=10, sticky="w")
            self.form_entries[label_text] = entry
        if item:
            self.form_entries["Item Name"].insert(0, item.get("product_name", ""))
            self.form_entries["SKU"].insert(0, str(item.get("sku", "")))
            self.form_entries["Category"].set(item.get("category", ""))
            self.form_entries["Grams"].insert(0, str(item.get("grams", "")))
            self.form_entries["CTW Diamond"].insert(0, str(item.get("ctw_diamond", "")))
            self.form_entries["Number of Pieces"].insert(0, str(item.get("number_of_pcs", "")))
            self.form_entries["Reference Cost"].insert(0, str(item.get("reference_cost", "")))
            self.form_entries["Our Cost"].insert(0, str(item.get("our_cost", "")))
            self.image_path = item.get("image_path", None)
        else:
            self.form_entries["SKU"].insert(0, str(self.sku_counter))
        save_btn = ctk.CTkButton(self, text="💾 Save Item 💾", corner_radius=10, command=save_command, width=200, height=40)
        save_btn.pack(pady=20)
        back_btn = ctk.CTkButton(self, text="🔙 Back to Home 🔙", corner_radius=10, command=self.setup_home_screen, width=200, height=40)
        back_btn.pack(pady=10)

    def upload_image(self, label):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image_path = file_path
            img = Image.open(file_path)
            img.thumbnail((100, 100))
            img_tk = ImageTk.PhotoImage(img)
            label.configure(image=img_tk)
            label.image = img_tk

    def save_new_item(self):
        try:
            new_item = {
                "product_name": self.form_entries["Item Name"].get(),
                "sku": self.sku_counter,
                "category": self.form_entries["Category"].get(),
                "grams": float(self.form_entries["Grams"].get()),
                "ctw_diamond": float(self.form_entries["CTW Diamond"].get()),
                "number_of_pcs": int(self.form_entries["Number of Pieces"].get()),
                "reference_cost": float(self.form_entries["Reference Cost"].get()),
                "our_cost": float(self.form_entries["Our Cost"].get()),
                "image_path": self.image_path,
            }
            items_collection.insert_one(new_item)
            self.log_activity(f"Added new item {new_item['product_name']} (SKU: {new_item['sku']})")
            self.sku_counter += 1
            self.inventory.append(new_item)
            messagebox.showinfo("✅ Success ✅", "Item added successfully!")
            self.setup_home_screen()
        except ValueError as e:
            messagebox.showerror("❌ Error ❌", f"Invalid input: {e}")

    def show_qr_code(self, item):
        qr_content = f"Item Name: {item['product_name']}\nSKU: {item['sku']}\nCategory: {item['category']}\nStock: {item['number_of_pcs']}"

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_content)
        qr.make(fit=True)

        qr_img = qr.make_image(fill="black", back_color="white")

        qr_img_path = os.path.join(os.getcwd(), "temp_qr_code.png")
        qr_img.save(qr_img_path)

        qr_window = ctk.CTkToplevel(self)
        qr_window.title(f"QR Code for {item['product_name']} (SKU: {item['sku']})")

        qr_ctk_image = CTkImage(light_image=Image.open(qr_img_path), size=(200, 200))

        qr_label = ctk.CTkLabel(qr_window, image=qr_ctk_image)
        qr_label.pack(pady=20)

        close_btn = ctk.CTkButton(qr_window, text="❌ Close ❌", command=qr_window.destroy)
        close_btn.pack(pady=10)

    def show_inventory_context_menu(self, event):
        menu = Menu(self, tearoff=0)

        item_id = self.tree.identify_row(event.y)
        if item_id:
            self.tree.selection_set(item_id)
            selected_item = self.tree.item(item_id, "values")
            sku = selected_item[1]
            item = items_collection.find_one({"sku": int(sku)})

            if self.current_user['role'] == 'admin':
                menu.add_command(label="✏ Edit Item ✏", command=lambda: self.edit_item_screen(item))
                menu.add_command(label="❌ Delete Item ❌", command=lambda: self.delete_item(item))
                menu.add_command(label="📦 Add Quantity 📦", command=lambda: self.show_add_pieces_screen(item))

            menu.add_command(label="✔ Sell Item ✔", command=lambda: self.show_item_sold_details(item))
            menu.add_command(label="📄 Generate QR Code 📄", command=lambda: self.show_qr_code(item))

            menu.post(event.x_root, event.y_root)

    def delete_item(self, item):
        confirm = messagebox.askyesno("🗑️ Confirm Delete 🗑️", f"Are you sure you want to delete {item['product_name']}?")
        if confirm:
            items_collection.delete_one({"sku": item['sku']})
            messagebox.showinfo("🗑️ Deleted 🗑️", f"Item {item['product_name']} deleted!")
            self.setup_home_screen()

    def show_item_sold_details(self, item):
        self.clear_widgets()
        header = ctk.CTkLabel(self, text=f"🛍️ Item 🛍️: {item['product_name']} (SKU: {item['sku']})", font=("Arial", 24, "bold"), text_color="white")
        header.pack(pady=20)
        if item.get("image_path") and os.path.exists(item["image_path"]):
            img = Image.open(item["image_path"])
            img.thumbnail((200, 200))
            img_tk = ImageTk.PhotoImage(img)
            img_label = ctk.CTkLabel(self, image=img_tk)
            img_label.image = img_tk
            img_label.pack(pady=10)
        ctk.CTkLabel(self, text=f"📊 Current Stock 📊: {item['number_of_pcs']}", font=("Arial", 18), text_color="white").pack(pady=10)
        sold_var = ctk.CTkEntry(self, placeholder_text="🔢 Enter number of pieces sold 🔢")
        sold_var.pack(pady=10)

        def confirm_sale():
            try:
                pieces_sold = int(sold_var.get())
                if pieces_sold > item['number_of_pcs']:
                    raise ValueError("Cannot sell more than available stock.")
                new_stock = item['number_of_pcs'] - pieces_sold
                items_collection.update_one({"sku": item['sku']}, {"$set": {"number_of_pcs": new_stock}})
                self.log_activity(f"Sold {pieces_sold} pieces of {item['product_name']} (SKU: {item['sku']})")
                self.record_transaction(item, pieces_sold)  # Record sale in transactions collection
                messagebox.showinfo("✅ Success ✅", "Sale confirmed and transaction recorded.")
                self.setup_home_screen()
            except ValueError as e:
                messagebox.showerror("❌ Error ❌", f"Invalid input: {e}")

        confirm_btn = ctk.CTkButton(self, text="✔ Confirm Sale ✔", corner_radius=10, command=confirm_sale, width=200, height=40)
        confirm_btn.pack(pady=10)
        back_btn = ctk.CTkButton(self, text="🔙 Back to Home 🔙", corner_radius=10, command=self.setup_home_screen, width=200, height=40)
        back_btn.pack(pady=10)

    def record_transaction(self, item, pieces_sold):
        transaction = {
            "item_sku": item['sku'],
            "item_name": item['product_name'],
            "quantity_sold": pieces_sold,
            "unit_price": item['our_cost'],
            "total_cost": pieces_sold * item['our_cost'],
            "date": datetime.datetime.now()
        }
        transactions_collection.insert_one(transaction)

    def add_quantity_screen(self):
        self.clear_widgets()
        header = ctk.CTkLabel(self, text="📦 Add Quantity to Existing Item 📦", font=("Arial", 30, "bold"), text_color="white")
        header.pack(pady=20)
        search_var = ctk.CTkEntry(self, width=400, placeholder_text="🔍 Enter SKU or Item Name 🔍")
        search_var.pack(pady=10)

        def search_item():
            query = search_var.get()
            try:
                if query.isdigit():
                    item = items_collection.find_one({"sku": int(query)})
                else:
                    item = items_collection.find_one({"product_name": {"$regex": f"^{query}$", "$options": "i"}})
                if item:
                    self.show_add_pieces_screen(item)
                else:
                    messagebox.showerror("❌ Error ❌", "Item not found.")
            except Exception as e:
                messagebox.showerror("❌ Error ❌", f"Invalid search input. {e}")

        search_btn = ctk.CTkButton(self, text="🔍 Search Item 🔍", corner_radius=10, command=search_item, width=200, height=40)
        search_btn.pack(pady=10)
        back_btn = ctk.CTkButton(self, text="🔙 Back to Home 🔙", corner_radius=10, command=self.setup_home_screen, width=200, height=40)
        back_btn.pack(pady=10)

    def show_add_pieces_screen(self, item):
        self.clear_widgets()
        header = ctk.CTkLabel(self, text=f"📦 Add Pieces to Item 📦: {item['product_name']} (SKU: {item['sku']})", font=("Arial", 24, "bold"), text_color="white")
        header.pack(pady=20)
        if item.get("image_path") and os.path.exists(item["image_path"]):
            img = Image.open(item["image_path"])
            img.thumbnail((200, 200))
            img_tk = ImageTk.PhotoImage(img)
            img_label = ctk.CTkLabel(self, image=img_tk)
            img_label.image = img_tk
            img_label.pack(pady=10)
        ctk.CTkLabel(self, text=f"📊 Current Stock 📊: {item['number_of_pcs']}", font=("Arial", 18), text_color="white").pack(pady=10)
        quantity_var = ctk.CTkEntry(self, placeholder_text="🔢 Enter number of pieces to add 🔢")
        quantity_var.pack(pady=10)

        def confirm_add_pieces():
            try:
                pieces_to_add = int(quantity_var.get())
                new_stock = item['number_of_pcs'] + pieces_to_add
                items_collection.update_one({"sku": item['sku']}, {"$set": {"number_of_pcs": new_stock}})
                self.log_activity(f"Added {pieces_to_add} pieces to {item['product_name']} (SKU: {item['sku']})")
                messagebox.showinfo("✅ Success ✅", f"Added {pieces_to_add} pieces to SKU {item['sku']}.")
                self.setup_home_screen()
            except ValueError as e:
                messagebox.showerror("❌ Error ❌", f"Invalid input: {e}")

        confirm_btn = ctk.CTkButton(self, text="✔ Confirm ✔", corner_radius=10, command=confirm_add_pieces, width=200, height=40)
        confirm_btn.pack(pady=10)
        back_btn = ctk.CTkButton(self, text="🔙 Back to Home 🔙", corner_radius=10, command=self.setup_home_screen, width=200, height=40)
        back_btn.pack(pady=10)

    def edit_item_screen(self, item):
        self.clear_widgets()
        header = ctk.CTkLabel(self, text="✏ Edit Item ✏", font=("Arial", 30, "bold"), text_color="white")
        header.pack(pady=20)
        self.create_item_form(lambda: self.save_item_changes(item), item)

    def save_item_changes(self, original_item):
        try:
            updated_item = {
                "product_name": self.form_entries["Item Name"].get(),
                "sku": original_item['sku'],
                "category": self.form_entries["Category"].get(),
                "grams": float(self.form_entries["Grams"].get()),
                "ctw_diamond": float(self.form_entries["CTW Diamond"].get()),
                "number_of_pcs": int(self.form_entries["Number of Pieces"].get()),
                "reference_cost": float(self.form_entries["Reference Cost"].get()),
                "our_cost": float(self.form_entries["Our Cost"].get()),
                "image_path": self.image_path,
            }
            items_collection.update_one({"sku": original_item['sku']}, {"$set": updated_item})
            self.log_activity(f"Updated item {updated_item['product_name']} (SKU: {updated_item['sku']})")
            messagebox.showinfo("✅ Success ✅", "Item updated successfully!")
            self.setup_home_screen()
        except ValueError as e:
            messagebox.showerror("❌ Error ❌", f"Invalid input: {e}")

    def manage_users_screen(self):
        self.clear_widgets()

        header = ctk.CTkLabel(self, text="👤 Manage Users 👤", font=("Arial", 36, "bold"), text_color="white")
        header.pack(pady=20)

        search_frame = ctk.CTkFrame(self, fg_color="#2C2F33", corner_radius=10)
        search_frame.pack(pady=10, padx=20, fill="x")

        search_entry = ctk.CTkEntry(search_frame, placeholder_text="🔍 Search by Name/Username 🔍", width=400)
        search_entry.grid(row=0, column=0, padx=10, pady=10)
        search_entry.bind("<KeyRelease>", self.search_users)

        # Add the Add User button to the screen
        add_user_btn = ctk.CTkButton(search_frame, text="➕ Add User ➕", corner_radius=10, command=self.add_user_screen, width=200)
        add_user_btn.grid(row=0, column=1, padx=10, pady=10)

        self.search_entry = search_entry

        self.user_frame = ctk.CTkFrame(self, fg_color="#2C2F33", corner_radius=10)
        self.user_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.show_users_table(self.user_frame)

        back_btn = ctk.CTkButton(self, text="🔙 Back to Home 🔙", corner_radius=10, command=self.setup_home_screen, width=200, height=40)
        back_btn.pack(pady=10)

    def add_user_screen(self):
        self.clear_widgets()

        header = ctk.CTkLabel(self, text="➕ Add New User ➕", font=("Arial", 36, "bold"), text_color="white")
        header.pack(pady=20)

        name_entry = ctk.CTkEntry(self, placeholder_text="👤 Name 👤", width=300)
        name_entry.pack(pady=10)
        
        username_entry = ctk.CTkEntry(self, placeholder_text="👤 Username 👤", width=300)
        username_entry.pack(pady=10)
        
        password_entry = ctk.CTkEntry(self, placeholder_text="🔑 Password 🔑", show="*", width=300)
        password_entry.pack(pady=10)

        # Add Role dropdown selection
        role_label = ctk.CTkLabel(self, text="🔑 Role 🔑", font=("Arial", 16), text_color="white")
        role_label.pack(pady=10)
        
        role_selection = ctk.CTkComboBox(self, values=["user", "admin"], width=300)
        role_selection.set("user")  # Default to 'user'
        role_selection.pack(pady=10)

        # Save the user data with the role
        def save_user():
            name = name_entry.get()
            username = username_entry.get()
            password = password_entry.get()
            role = role_selection.get()

            if len(password) < 6:
                messagebox.showerror("❌ Error ❌", "Password must be at least 6 characters long.")
                return
            if username and password and name and role:
                self.register_user(username, password, name, role)  # Include role when registering user
            else:
                messagebox.showerror("❌ Error ❌", "All fields are required.")
        
        save_btn = ctk.CTkButton(self, text="💾 Save User 💾", corner_radius=10, command=save_user, width=200, height=40)
        save_btn.pack(pady=10)
        
        back_btn = ctk.CTkButton(self, text="🔙 Back to Manage Users 🔙", corner_radius=10, command=self.manage_users_screen, width=200, height=40)
        back_btn.pack(pady=10)


    def search_users(self, *args):
        search_query = self.search_entry.get()
        query = {}
        if search_query:
            query["$or"] = [
                {"name": {"$regex": search_query, "$options": "i"}},
                {"username": {"$regex": search_query, "$options": "i"}},
            ]
        users = list(users_collection.find(query))
        for widget in self.user_frame.winfo_children():
            widget.destroy()
        self.show_users_table(self.user_frame, users)

    def show_users_table(self, parent, users=None):
        if users is None:
            users = list(users_collection.find())
        tree_scroll = ttk.Scrollbar(parent)
        tree_scroll.pack(side="right", fill="y")
        self.user_tree = ttk.Treeview(parent, columns=("Name", "Username", "Role"), show="headings", yscrollcommand=tree_scroll.set)
        self.user_tree.heading("Name", text="👤 Name 👤")
        self.user_tree.heading("Username", text="📛 Username 📛")
        self.user_tree.heading("Role", text="🔑 Role 🔑")
        self.user_tree.pack(fill="both", expand=True, padx=20, pady=10)
        tree_scroll.config(command=self.user_tree.yview)

        for user in users:
            self.user_tree.insert("", "end", values=(
                user['name'],
                user['username'],
                user['role']
            ))

        self.user_tree.bind("<Double-1>", self.show_context_menu)

    def show_context_menu(self, event):
        menu = Menu(self, tearoff=0)

        item = self.user_tree.identify_row(event.y)
        if item:
            self.user_tree.selection_set(item)
            selected_user = self.user_tree.item(item, "values")
            username = selected_user[1]
            user = users_collection.find_one({"username": username})

            if user['role'] == 'admin':
                menu.add_command(label="🔽 Demote to User 🔽", command=lambda: self.update_role(user, 'user'))
            else:
                menu.add_command(label="🔼 Promote to Admin 🔼", command=lambda: self.update_role(user, 'admin'))
            menu.add_separator()
            menu.add_command(label="❌ Delete User ❌", command=lambda: self.delete_user(user))

            menu.post(event.x_root, event.y_root)

    def update_role(self, user, new_role):
        users_collection.update_one({"username": user['username']}, {"$set": {"role": new_role}})
        messagebox.showinfo("✅ Success ✅", f"User {user['username']} updated to {new_role}!")
        self.manage_users_screen()

    def delete_user(self, user):
        users_collection.delete_one({"username": user['username']})
        messagebox.showinfo("🗑️ Deleted 🗑️", f"User {user['username']} deleted!")
        self.manage_users_screen()


    def clear_widgets(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.tree = None
        self.inventory_frame = None
        self.total_pieces_label = None
        self.total_cost_label = None

if __name__ == "__main__":
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("green")
    app = MainApp()
    app.mainloop()

