import customtkinter as ctk
from tkinter import filedialog, ttk, messagebox
from PIL import Image, ImageTk
import os
from pymongo import MongoClient
import hashlib

client = MongoClient('mongodb://localhost:27017/')
db = client['inventory_db']
items_collection = db['items']
users_collection = db['users']

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("🔐 Inventory Management System")
        self.geometry("1080x720")
        self.configure(bg="#1A1A1D")
        # self.resizable(False, False)
        self.image_path = None
        self.sku_counter = self.get_next_sku()
        self.inventory = list(items_collection.find())
        self.show_login_screen()

    def get_next_sku(self):
        last_item = items_collection.find_one(sort=[("sku", -1)])
        return last_item['sku'] + 1 if last_item else 100001

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def register_user(self, username, password, name):
        if users_collection.find_one({"username": username}):
            messagebox.showerror("Error", "Username already exists!")
            return False
        hashed_password = self.hash_password(password)
        users_collection.insert_one({
            "username": username,
            "password": hashed_password,
            "name": name
        })
        messagebox.showinfo("Success", "Registration successful!")
        self.show_login_screen()

    def authenticate_user(self, username, password):
        hashed_password = self.hash_password(password)
        user = users_collection.find_one({"username": username, "password": hashed_password})
        return True if user else False

    def show_login_screen(self):
        self.clear_widgets()
        header = ctk.CTkLabel(self, text="🔑 Login", font=("Arial", 36, "bold"), text_color="white")
        header.pack(pady=20)
        username_entry = ctk.CTkEntry(self, placeholder_text="👤 Username", width=300)
        username_entry.pack(pady=10)
        password_entry = ctk.CTkEntry(self, placeholder_text="🔒 Password", show="*", width=300)
        password_entry.pack(pady=10)

        def login():
            username = username_entry.get()
            password = password_entry.get()
            if self.authenticate_user(username, password):
                messagebox.showinfo("Success", "Login successful!")
                self.setup_home_screen()
            else:
                messagebox.showerror("Error", "Invalid username or password.")

        login_btn = ctk.CTkButton(self, text="🔓 Login", corner_radius=10, command=login, width=200, height=40)
        login_btn.pack(pady=10)
        register_btn = ctk.CTkButton(self, text="📝 Register", corner_radius=10, command=self.show_register_screen, width=200, height=40)
        register_btn.pack(pady=10)

    def show_register_screen(self):
        self.clear_widgets()
        header = ctk.CTkLabel(self, text="📝 Register", font=("Arial", 36, "bold"), text_color="white")
        header.pack(pady=20)
        name_entry = ctk.CTkEntry(self, placeholder_text="👤 Name", width=300)
        name_entry.pack(pady=10)
        username_entry = ctk.CTkEntry(self, placeholder_text="📛 Username", width=300)
        username_entry.pack(pady=10)
        password_entry = ctk.CTk.CTkEntry(self, placeholder_text="🔑 Password", show="*", width=300)
        password_entry.pack(pady=10)

        def register():
            name = name_entry.get()
            username = username_entry.get()
            password = password_entry.get()
            if len(password) < 6:
                messagebox.showerror("Error", "Password must be at least 6 characters long.")
                return
            if username and password and name:
                self.register_user(username, password, name)
            else:
                messagebox.showerror("Error", "All fields are required.")

        register_btn = ctk.CTkButton(self, text="📝 Register", corner_radius=10, command=register, width=200, height=40)
        register_btn.pack(pady=10)
        back_btn = ctk.CTkButton(self, text="🔙 Back to Login", corner_radius=10, command=self.show_login_screen, width=200, height=40)
        back_btn.pack(pady=10)

    def setup_home_screen(self):
        self.clear_widgets()
        header = ctk.CTkLabel(self, text="🏠 Inventory System", font=("Arial", 36, "bold"), text_color="white")
        header.pack(pady=20)
        
        # Create a frame for search and filter bar
        search_filter_frame = ctk.CTkFrame(self, fg_color="#2C2F33", corner_radius=10)
        search_filter_frame.pack(pady=10, padx=20, fill="x")

        # Search entry
        search_entry = ctk.CTkEntry(search_filter_frame, placeholder_text="🔍 Search by Name/SKU", width=400)
        search_entry.grid(row=0, column=0, padx=10, pady=10)

        # Filter by category
        filter_category = ctk.CTkComboBox(search_filter_frame, width=200, values=["All", "Rings", "Necklaces", "Bracelets", "Watches"])
        filter_category.grid(row=0, column=1, padx=10, pady=10)

        # Live search function
        def live_search(event=None):
            search_query = search_entry.get()
            category = filter_category.get()
            query = {}
            
            if search_query:
                query["$or"] = [
                    {"sku": int(search_query)} if search_query.isdigit() else {},
                    {"product_name": {"$regex": search_query, "$options": "i"}}
                ]
            if category != "All":
                query["category"] = category
            
            self.inventory = list(items_collection.find(query))
            self.create_inventory_overview()


        search_entry.bind("<KeyRelease>", live_search)
        filter_category.bind("<<ComboboxSelected>>", live_search)

        self.create_inventory_overview()

        button_frame = ctk.CTkFrame(self, fg_color="#2C2F33", corner_radius=10)
        button_frame.pack(pady=30, padx=20, fill="x")

        add_item_btn = ctk.CTkButton(button_frame, text="➕ Add New Item", corner_radius=10, command=self.add_item_screen, width=200, height=40)
        add_item_btn.grid(row=0, column=0, padx=20, pady=10)

        add_quantity_btn = ctk.CTkButton(button_frame, text="📦 Add Quantity", corner_radius=10, command=self.add_quantity_screen, width=200, height=40)
        add_quantity_btn.grid(row=0, column=1, padx=20, pady=10)

        item_sold_btn = ctk.CTkButton(button_frame, text="✔ Mark Item as Sold", corner_radius=10, command=self.item_sold_screen, width=200, height=40)
        item_sold_btn.grid(row=0, column=2, padx=20, pady=10)

    def create_inventory_overview(self):
        inventory_frame = ctk.CTkFrame(self, fg_color="#2C2F33", corner_radius=10)
        inventory_frame.pack(pady=20, padx=20, fill="both", expand=True)
        total_pieces = sum(item['number_of_pcs'] for item in self.inventory)
        total_cost = sum(item['our_cost'] * item['number_of_pcs'] for item in self.inventory)
        total_pieces_label = ctk.CTkLabel(inventory_frame, text=f"📦 Total Pieces: {total_pieces}", text_color="white", font=("Arial", 18))
        total_pieces_label.pack(pady=10)
        total_cost_label = ctk.CTkLabel(inventory_frame, text=f"💲 Total Cost: ${total_cost:.2f}", text_color="white", font=("Arial", 18))
        total_cost_label.pack(pady=10)
        self.show_inventory_table(inventory_frame)

    def show_inventory_table(self, parent):
        tree_scroll = ttk.Scrollbar(parent)
        tree_scroll.pack(side="right", fill="y")
        tree = ttk.Treeview(parent, columns=("Item", "SKU", "Category", "Cost", "Stock"), show="headings", yscrollcommand=tree_scroll.set)
        tree.heading("Item", text="🛍️ Item")
        tree.heading("SKU", text="📦 SKU")
        tree.heading("Category", text="🏷️ Category")
        tree.heading("Cost", text="💰 Cost")
        tree.heading("Stock", text="📊 Stock")
        tree.column("Item", anchor="w", width=150)
        tree.column("SKU", anchor="center", width=100)
        tree.column("Category", anchor="center", width=100)
        tree.column("Cost", anchor="center", width=100)
        tree.column("Stock", anchor="center", width=100)
        for item in self.inventory:
            tree.insert("", "end", values=(
                item.get("product_name", ""),
                item.get("sku", ""),
                item.get("category", ""),
                f"${item.get('our_cost', 0):.2f}",
                item.get("number_of_pcs", 0),
            ))
        tree.pack(fill="both", expand=True, padx=20, pady=10)
        tree_scroll.config(command=tree.yview)
        tree.bind("<Double-1>", lambda e: self.on_item_double_click(tree))


    def on_item_double_click(self, tree):
        selected_item = tree.item(tree.selection()[0], "values")
        sku = selected_item[1]
        item = items_collection.find_one({"sku": int(sku)})
        self.edit_item_screen(item)

    def add_item_screen(self):
        self.clear_widgets()
        header = ctk.CTkLabel(self, text="➕ Add New Inventory Item", font=("Arial", 30, "bold"), text_color="white")
        header.pack(pady=20)
        self.create_item_form(self.save_new_item)

    def create_item_form(self, save_command, item=None):
        form_frame = ctk.CTkFrame(self, fg_color="#2C2F33", corner_radius=10)
        form_frame.pack(pady=20, padx=20, fill="both", expand=True)
        img_label = ctk.CTkLabel(form_frame, text="🖼️ No Image Uploaded", text_color="white", width=200)
        img_label.grid(row=0, column=1, padx=20, pady=10)
        img_btn = ctk.CTkButton(form_frame, text="📤 Upload Image", corner_radius=10, command=lambda: self.upload_image(img_label), width=200)
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
        save_btn = ctk.CTkButton(self, text="💾 Save Item", corner_radius=10, command=save_command, width=200, height=40)
        save_btn.pack(pady=20)
        back_btn = ctk.CTkButton(self, text="🔙 Back to Home", corner_radius=10, command=self.setup_home_screen, width=200, height=40)
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
            self.sku_counter += 1
            self.inventory.append(new_item)
            messagebox.showinfo("Success", "Item added successfully!")
            self.setup_home_screen()
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    def item_sold_screen(self):
        self.clear_widgets()
        header = ctk.CTkLabel(self, text="✔ Mark Item as Sold", font=("Arial", 30, "bold"), text_color="white")
        header.pack(pady=20)
        search_var = ctk.CTkEntry(self, width=400, placeholder_text="🔍 Enter SKU or Item Name")
        search_var.pack(pady=10)

        def search_item():
            query = search_var.get()
            try:
                item = items_collection.find_one({"$or": [{"sku": int(query)}, {"product_name": query}]})
                if item:
                    self.show_item_sold_details(item)
                else:
                    messagebox.showerror("Error", "Item not found.")
            except:
                messagebox.showerror("Error", "Invalid search input. Enter valid SKU or Item Name.")

        search_btn = ctk.CTkButton(self, text="🔍 Search Item", corner_radius=10, command=search_item, width=200, height=40)
        search_btn.pack(pady=10)
        back_btn = ctk.CTkButton(self, text="🔙 Back to Home", corner_radius=10, command=self.setup_home_screen, width=200, height=40)
        back_btn.pack(pady=10)

    def show_item_sold_details(self, item):
        self.clear_widgets()
        header = ctk.CTkLabel(self, text=f"🛍️ Item: {item['product_name']} (SKU: {item['sku']})", font=("Arial", 24, "bold"), text_color="white")
        header.pack(pady=20)
        if item.get("image_path") and os.path.exists(item["image_path"]):
            img = Image.open(item["image_path"])
            img.thumbnail((200, 200))
            img_tk = ImageTk.PhotoImage(img)
            img_label = ctk.CTkLabel(self, image=img_tk)
            img_label.image = img_tk
            img_label.pack(pady=10)
        ctk.CTkLabel(self, text=f"📊 Current Stock: {item['number_of_pcs']}", font=("Arial", 18), text_color="white").pack(pady=10)
        sold_var = ctk.CTkEntry(self, placeholder_text="🔢 Enter number of pieces sold")
        sold_var.pack(pady=10)

        def confirm_sale():
            try:
                pieces_sold = int(sold_var.get())
                if pieces_sold > item['number_of_pcs']:
                    raise ValueError("Cannot sell more than available stock.")
                new_stock = item['number_of_pcs'] - pieces_sold
                items_collection.update_one({"sku": item['sku']}, {"$set": {"number_of_pcs": new_stock}})
                messagebox.showinfo("Success", "Sale confirmed.")
                self.setup_home_screen()
            except ValueError as e:
                messagebox.showerror("Error", f"Invalid input: {e}")

        confirm_btn = ctk.CTkButton(self, text="✔ Confirm Sale", corner_radius=10, command=confirm_sale, width=200, height=40)
        confirm_btn.pack(pady=10)
        back_btn = ctk.CTkButton(self, text="🔙 Back to Home", corner_radius=10, command=self.setup_home_screen, width=200, height=40)
        back_btn.pack(pady=10)

    def add_quantity_screen(self):
        self.clear_widgets()
        header = ctk.CTkLabel(self, text="📦 Add Quantity to Existing Item", font=("Arial", 30, "bold"), text_color="white")
        header.pack(pady=20)
        search_var = ctk.CTkEntry(self, width=400, placeholder_text="🔍 Enter SKU or Item Name")
        search_var.pack(pady=10)

        def search_item():
            query = search_var.get()
            try:
                item = items_collection.find_one({"$or": [{"sku": int(query)}, {"product_name": query}]})
                if item:
                    self.show_add_pieces_screen(item)
                else:
                    messagebox.showerror("Error", "Item not found.")
            except:
                messagebox.showerror("Error", "Invalid search input. Enter valid SKU or Item Name.")

        search_btn = ctk.CTkButton(self, text="🔍 Search Item", corner_radius=10, command=search_item, width=200, height=40)
        search_btn.pack(pady=10)
        back_btn = ctk.CTkButton(self, text="🔙 Back to Home", corner_radius=10, command=self.setup_home_screen, width=200, height=40)
        back_btn.pack(pady=10)

    def show_add_pieces_screen(self, item):
        self.clear_widgets()
        header = ctk.CTkLabel(self, text=f"📦 Add Pieces to Item: {item['product_name']} (SKU: {item['sku']})", font=("Arial", 24, "bold"), text_color="white")
        header.pack(pady=20)
        if item.get("image_path") and os.path.exists(item["image_path"]):
            img = Image.open(item["image_path"])
            img.thumbnail((200, 200))
            img_tk = ImageTk.PhotoImage(img)
            img_label = ctk.CTkLabel(self, image=img_tk)
            img_label.image = img_tk
            img_label.pack(pady=10)
        ctk.CTkLabel(self, text=f"📊 Current Stock: {item['number_of_pcs']}", font=("Arial", 18), text_color="white").pack(pady=10)
        quantity_var = ctk.CTkEntry(self, placeholder_text="🔢 Enter number of pieces to add")
        quantity_var.pack(pady=10)

        def confirm_add_pieces():
            try:
                pieces_to_add = int(quantity_var.get())
                new_stock = item['number_of_pcs'] + pieces_to_add
                items_collection.update_one({"sku": item['sku']}, {"$set": {"number_of_pcs": new_stock}})
                messagebox.showinfo("Success", f"Added {pieces_to_add} pieces to SKU {item['sku']}.")
                self.setup_home_screen()
            except ValueError as e:
                messagebox.showerror("Error", f"Invalid input: {e}")

        confirm_btn = ctk.CTkButton(self, text="✔ Confirm", corner_radius=10, command=confirm_add_pieces, width=200, height=40)
        confirm_btn.pack(pady=10)
        back_btn = ctk.CTkButton(self, text="🔙 Back to Home", corner_radius=10, command=self.setup_home_screen, width=200, height=40)
        back_btn.pack(pady=10)

    def edit_item_screen(self, item):
        self.clear_widgets()
        header = ctk.CTkLabel(self, text="✏ Edit Item", font=("Arial", 30, "bold"), text_color="white")
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
            messagebox.showinfo("Success", "Item updated successfully!")
            self.setup_home_screen()
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    def clear_widgets(self):
        for widget in self.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")
    app = MainApp()
    app.mainloop()
