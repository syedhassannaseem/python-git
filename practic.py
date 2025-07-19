# tkinter_ui_inventory.py
import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
import random
import string
import time
from datetime import datetime
from win10toast import ToastNotifier

INVENTORYFILE = "inventory.json"
HISTORYFILE = "Sales_History.json"

def dump_inventory(inventory):
    with open(INVENTORYFILE, "w") as f:
        json.dump(inventory, f, indent=4)

def load_inventory():
    if os.path.exists(INVENTORYFILE):
        with open(INVENTORYFILE, "r") as f:
            return json.load(f)
    return {}

def dump_sale(sale):
    with open(HISTORYFILE, "w") as f:
        json.dump(sale, f, indent=4)

def load_sale():
    if os.path.exists(HISTORYFILE):
        with open(HISTORYFILE, "r") as f:
            return json.load(f)
    return {}

class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System")
        self.root.geometry("700x500")

        label = tk.Label(root, text="Inventory Management System", font=("Arial", 20, "bold"), pady=20)
        label.pack()

        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=20)

        buttons = [
            ("Add Product", self.add_product_ui),
            ("Process Sale", self.process_sale_ui),
            ("Update Stock", self.update_stock_ui),
            ("View Inventory", self.view_inventory_ui),
            ("View History", self.view_history_ui),
            ("Delete Inventory", self.delete_inventory),
        ]

        for text, command in buttons:
            btn = tk.Button(btn_frame, text=text, command=command, width=20, pady=5)
            btn.pack(pady=5)

        self.check_stock_notification()

    def add_product_ui(self):
        self.clear_window()
        frame = tk.Frame(self.root)
        frame.pack(pady=20)

        labels = ["Product ID", "Name", "Quantity", "Price", "Batch No"]
        entries = {}

        for i, label in enumerate(labels):
            tk.Label(frame, text=label).grid(row=i, column=0, sticky='e')
            entry = tk.Entry(frame)
            entry.grid(row=i, column=1)
            entries[label] = entry

        def save_product():
            inventory = load_inventory()
            ID = entries["Product ID"].get()
            if ID in inventory:
                messagebox.showwarning("Warning", "Product ID already exists")
                return
            try:
                Quantity = int(entries["Quantity"].get())
                Price = float(entries["Price"].get())
            except ValueError:
                messagebox.showerror("Error", "Quantity must be integer and Price must be float")
                return

            inventory[ID] = {
                "Name": entries["Name"].get(),
                "Quantity": Quantity,
                "Price": Price,
                "Batch_No": entries["Batch No"].get()
            }
            dump_inventory(inventory)
            messagebox.showinfo("Success", "Product Added Successfully")

        tk.Button(frame, text="Save", command=save_product).grid(row=5, columnspan=2, pady=10)

    def view_inventory_ui(self):
        self.clear_window()
        data = load_inventory()
        if not data:
            messagebox.showinfo("Info", "No Inventory Found")
            return

        tree = ttk.Treeview(self.root, columns=("ID", "Name", "Qty", "Price", "Total", "Batch"), show="headings")
        for col in tree["columns"]:
            tree.heading(col, text=col)

        for ID, d in data.items():
            total = d["Quantity"] * d["Price"]
            tree.insert('', 'end', values=(ID, d["Name"], d["Quantity"], d["Price"], total, d["Batch_No"]))
        tree.pack(expand=True, fill='both', padx=10, pady=10)

    def view_history_ui(self):
        self.clear_window()
        data = load_sale()
        if not data:
            messagebox.showinfo("Info", "No Sales History Found")
            return

        tree = ttk.Treeview(self.root, columns=("ID", "City", "Name", "Qty", "Unit Price", "Total", "Date", "Time"), show="headings")
        for col in tree["columns"]:
            tree.heading(col, text=col)

        for ID, d in data.items():
            tree.insert('', 'end', values=(ID, d["City"], d["Name"], d["Quantity"], d["Unit_Price"], d["Total_Price"], d["Date"], d["Time"]))
        tree.pack(expand=True, fill='both', padx=10, pady=10)

    def process_sale_ui(self):
        self.clear_window()
        frame = tk.Frame(self.root)
        frame.pack(pady=20)

        tk.Label(frame, text="Enter Product ID:").grid(row=0, column=0)
        id_entry = tk.Entry(frame)
        id_entry.grid(row=0, column=1)

        tk.Label(frame, text="Enter City:").grid(row=1, column=0)
        city_entry = tk.Entry(frame)
        city_entry.grid(row=1, column=1)

        tk.Label(frame, text="Quantity to Sell:").grid(row=2, column=0)
        qty_entry = tk.Entry(frame)
        qty_entry.grid(row=2, column=1)

        def sell():
            ID = id_entry.get()
            city = city_entry.get()
            try:
                qty = int(qty_entry.get())
            except ValueError:
                messagebox.showerror("Error", "Quantity must be an integer")
                return

            inventory = load_inventory()
            if ID not in inventory:
                messagebox.showerror("Error", "Product ID not found")
                return

            if inventory[ID]["Quantity"] < qty:
                messagebox.showwarning("Warning", "Not enough stock")
                return

            inventory[ID]["Quantity"] -= qty
            dump_inventory(inventory)

            total = qty * inventory[ID]["Price"]
            invo = ''.join(random.choices(string.ascii_letters, k=4))
            history = load_sale()
            history[invo] = {
                "ID": ID,
                "City": city,
                "Name": inventory[ID]["Name"],
                "Quantity": qty,
                "Unit_Price": inventory[ID]["Price"],
                "Total_Price": total,
                "Date": time.strftime("%d-%B-%Y"),
                "Time": str(datetime.now().time())
            }
            dump_sale(history)
            messagebox.showinfo("Success", f"Sale completed. Total = Rs{total}")

        tk.Button(frame, text="Process Sale", command=sell).grid(row=3, columnspan=2, pady=10)

    def update_stock_ui(self):
        self.clear_window()
        frame = tk.Frame(self.root)
        frame.pack(pady=20)

        tk.Label(frame, text="Product ID:").grid(row=0, column=0)
        id_entry = tk.Entry(frame)
        id_entry.grid(row=0, column=1)

        tk.Label(frame, text="Quantity to Add/Subtract:").grid(row=1, column=0)
        qty_entry = tk.Entry(frame)
        qty_entry.grid(row=1, column=1)

        def update():
            ID = id_entry.get()
            try:
                qty = int(qty_entry.get())
            except ValueError:
                messagebox.showerror("Error", "Quantity must be integer")
                return

            inventory = load_inventory()
            if ID not in inventory:
                messagebox.showerror("Error", "Product not found")
                return

            inventory[ID]["Quantity"] += qty
            dump_inventory(inventory)
            messagebox.showinfo("Success", "Quantity Updated")

        tk.Button(frame, text="Update", command=update).grid(row=2, columnspan=2, pady=10)

    def delete_inventory(self):
        if messagebox.askyesno("Confirm", "Are you sure to delete all inventory data?"):
            with open(INVENTORYFILE, 'w') as f:
                json.dump({}, f)
            messagebox.showinfo("Deleted", "Inventory content cleared")

    def check_stock_notification(self):
        data = load_inventory()
        toaster = ToastNotifier()
        for ID, item in data.items():
            if item["Quantity"] <= 500:
                toaster.show_toast("Stock Alert", f"{item['Name']} is low on stock (Only {item['Quantity']} left)", duration=3, threaded=True)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        label = tk.Label(self.root, text="Inventory Management System", font=("Arial", 20, "bold"), pady=20)
        label.pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryApp(root)
    root.mainloop()
