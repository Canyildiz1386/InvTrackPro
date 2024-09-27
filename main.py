import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
import pymongo

# MongoDB connection setup
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["InventoryDB"]
inventory_collection = db["InventoryItems"]

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1200x800")
        self.root.title("Modern Inventory System")
        self.root.configure(bg="#212121")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.setup_home_screen()

    def setup_home_screen(self):
        self.clear_screen()

        self.header = ctk.CTkLabel(self.root, text="Inventory Management", font=ctk.CTkFont(size=28, weight="bold"))
        self.header.pack(pady=20)

        total_pieces = self.calculate_total_pieces()
        self.total_pieces_label = ctk.CTkLabel(self.root, text=f"Total Pieces: {total_pieces}", font=ctk.CTkFont(size=16))
        self.total_pieces_label.pack(pady=10)

        total_cost = self.calculate_total_cost()
        self.total_cost_label = ctk.CTkLabel(self.root, text=f"Total Cost: ${total_cost:,.2f}", font=ctk.CTkFont(size=16))
        self.total_cost_label.pack(pady=10)

        self.filter_label = ctk.CTkLabel(self.root, text="Filter Items By:", font=ctk.CTkFont(size=14))
        self.filter_label.pack(pady=5)

        self.filter_var = ctk.StringVar()
        self.filter_options = ctk.CTkOptionMenu(self.root, variable=self.filter_var, values=['Most Sold', 'Least Quantity', 'In Stock', 'Out of Stock'], command=self.update_inventory_view)
        self.filter_options.pack(pady=5)

        self.search_var = ctk.StringVar()
        self.search_entry = ctk.CTkEntry(self.root, textvariable=self.search_var, placeholder_text="Search...", width=400, height=40)
        self.search_entry.pack(pady=10)
        self.search_var.trace_add("write", self.update_inventory_view)

        self.button_frame = ctk.CTkFrame(self.root)
        self.button_frame.pack(pady=10)

        self.new_item_button = ctk.CTkButton(self.button_frame, text="New Item", command=self.new_item_screen, width=200)
        self.new_item_button.grid(row=0, column=0, padx=10)

        self.update_button = ctk.CTkButton(self.button_frame, text="Update Item", command=self.add_quantity_screen, width=200)
        self.update_button.grid(row=0, column=1, padx=10)

        self.sold_button = ctk.CTkButton(self.button_frame, text="Mark as Sold", command=self.item_sold_screen, width=200)
        self.sold_button.grid(row=0, column=2, padx=10)

        self.inventory_frame = ctk.CTkFrame(self.root)
        self.inventory_frame.pack(pady=20, fill="both", expand=True)
        self.display_inventory()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def calculate_total_pieces(self):
        return sum(item.get("number_of_pcs", 0) for item in inventory_collection.find())

    def calculate_total_cost(self):
        return sum(item.get("our_cost", 0) * item.get("number_of_pcs", 0) for item in inventory_collection.find())

    def display_inventory(self):
        self.clear_inventory_view()

        self.inventory_list = ctk.CTkScrollableFrame(self.inventory_frame, width=1000, height=400)
        self.inventory_list.pack(fill="both", expand=True)

        for item in inventory_collection.find():
            self.add_inventory_row(item)

    def clear_inventory_view(self):
        for widget in self.inventory_frame.winfo_children():
            widget.destroy()

    def add_inventory_row(self, item):
        item_row = ctk.CTkFrame(self.inventory_list)
        item_row.pack(fill="x", pady=2)

        sku_label = ctk.CTkLabel(item_row, text=item['sku'], width=100, anchor="w")
        sku_label.grid(row=0, column=0, padx=10)

        name_label = ctk.CTkLabel(item_row, text=item['product_name'], width=200, anchor="w")
        name_label.grid(row=0, column=1, padx=10)

        pcs_label = ctk.CTkLabel(item_row, text=str(item['number_of_pcs']), width=100, anchor="center")
        pcs_label.grid(row=0, column=2, padx=10)

        cost_label = ctk.CTkLabel(item_row, text=f"${item['our_cost']:,.2f}", width=100, anchor="e")
        cost_label.grid(row=0, column=3, padx=10)

        sold_label = ctk.CTkLabel(item_row, text=str(item.get('pieces_sold', 0)), width=100, anchor="e")
        sold_label.grid(row=0, column=4, padx=10)

    def new_item_screen(self):
        self.clear_screen()

        self.header = ctk.CTkLabel(self.root, text="Add New Item", font=ctk.CTkFont(size=24, weight="bold"))
        self.header.pack(pady=20)

        self.form_frame = ctk.CTkFrame(self.root)
        self.form_frame.pack(pady=20)

        self.sku_label = ctk.CTkLabel(self.form_frame, text="SKU:")
        self.sku_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")

        self.sku_entry = ctk.CTkEntry(self.form_frame)
        self.sku_entry.grid(row=0, column=1, padx=10, pady=10)

        self.name_label = ctk.CTkLabel(self.form_frame, text="Product Name:")
        self.name_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")

        self.name_entry = ctk.CTkEntry(self.form_frame)
        self.name_entry.grid(row=1, column=1, padx=10, pady=10)

        self.category_label = ctk.CTkLabel(self.form_frame, text="Category:")
        self.category_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")

        self.category_var = ctk.StringVar()
        self.category_menu = ctk.CTkOptionMenu(self.form_frame, variable=self.category_var, values=['Rings', 'Necklaces', 'Bracelets', 'Earrings', 'Watches'])
        self.category_menu.grid(row=2, column=1, padx=10, pady=10)

        self.cost_label = ctk.CTkLabel(self.form_frame, text="Cost:")
        self.cost_label.grid(row=3, column=0, padx=10, pady=10, sticky="e")

        self.cost_entry = ctk.CTkEntry(self.form_frame)
        self.cost_entry.grid(row=3, column=1, padx=10, pady=10)

        self.pcs_label = ctk.CTkLabel(self.form_frame, text="Number of Pieces:")
        self.pcs_label.grid(row=4, column=0, padx=10, pady=10, sticky="e")

        self.pcs_entry = ctk.CTkEntry(self.form_frame)
        self.pcs_entry.grid(row=4, column=1, padx=10, pady=10)

        self.save_button = ctk.CTkButton(self.root, text="Save Item", command=self.save_item)
        self.save_button.pack(pady=20)

    def save_item(self):
        sku = self.sku_entry.get()
        product_name = self.name_entry.get()
        category = self.category_var.get()
        cost = float(self.cost_entry.get())
        pcs = int(self.pcs_entry.get())

        item = {
            'sku': sku,
            'product_name': product_name,
            'category': category,
            'our_cost': cost,
            'number_of_pcs': pcs,
            'pieces_sold': 0
        }
        inventory_collection.insert_one(item)
        self.setup_home_screen()

    def add_quantity_screen(self):
        pass

    def item_sold_screen(self):
        pass

    def update_inventory_view(self, *args):
        pass

if __name__ == "__main__":
    root = ctk.CTk()
    app = MainApp(root)
    root.mainloop()
