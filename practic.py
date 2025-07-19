import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import os
import random
import string
import time
from datetime import datetime

# File names
INVENTORYFILE = "inventory.json"
HISTORY = "Sales_History.json"

# Load and Dump Functions
def dump_inventory(inventory):
    with open(INVENTORYFILE, "w") as g:
        json.dump(inventory, g, indent=4)

def load_inventory():
    if os.path.exists(INVENTORYFILE):
        with open(INVENTORYFILE, "r") as h:
            return json.load(h)
    return {}

def dump_Sale(sale):
    with open(HISTORY, "w") as g:
        json.dump(sale, g, indent=4)

def load_Sale():
    if os.path.exists(HISTORY):
        with open(HISTORY, "r") as h:
            return json.load(h)
    return {}

# GUI Application
class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System")
        self.root.geometry("900x600")
        self.root.configure(bg="#f4f6f7")
        self.create_widgets()

    def create_widgets(self):
        title = tk.Label(self.root, text="Inventory Management System", font=("Arial", 20, "bold"), bg="#2e86de", fg="white", pady=10)
        title.pack(fill=tk.X)

        button_frame = tk.Frame(self.root, bg="#dcdde1")
        button_frame.pack(fill=tk.X, pady=5)

        buttons = [
            ("Add Product", self.add_inventory),
            ("Process Sale", self.process_sale),
            ("Update Stock", self.update_stock),
            ("View Inventory", self.view_inventory),
            ("View History", self.view_history),
            ("Delete Inventory", self.delete_inventory)
        ]

        for text, command in buttons:
            tk.Button(button_frame, text=text, command=command, font=("Arial", 11), bg="#0984e3", fg="white", width=15).pack(side=tk.LEFT, padx=5, pady=5)

        self.output = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, height=25, font=("Arial", 10))
        self.output.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def print_output(self, text):
        self.output.delete(1.0, tk.END)
        self.output.insert(tk.END, text)

    def add_inventory(self):
        def save():
            ID = entry_id.get()
            Name = entry_name.get()
            Quantity = entry_qty.get()
            Price = entry_price.get()
            Batch_No = entry_batch.get()

            if not ID or not Name or not Quantity or not Price or not Batch_No:
                messagebox.showerror("Input Error", "All fields are required!")
                return

            try:
                Quantity = int(Quantity)
                Price = float(Price)
            except ValueError:
                messagebox.showerror("Input Error", "Quantity must be integer and Price must be float!")
                return

            inventory = load_inventory()
            if ID in inventory:
                messagebox.showerror("Error", f"Product ID '{ID}' already exists!")
                return

            inventory[ID] = {
                "Name": Name,
                "Quantity": Quantity,
                "Price": Price,
                "Batch_No": Batch_No
            }
            dump_inventory(inventory)
            messagebox.showinfo("Success", "Product added successfully!")
            top.destroy()

        top = tk.Toplevel(self.root)
        top.title("Add Product")
        top.geometry("350x300")
        top.configure(bg="#dfe6e9")

        labels = ["Product ID", "Name", "Quantity", "Price", "Batch No"]
        entries = []

        for i, label in enumerate(labels):
            tk.Label(top, text=label, bg="#dfe6e9").grid(row=i, column=0, padx=10, pady=5, sticky="e")
        entry_id = tk.Entry(top); entry_id.grid(row=0, column=1)
        entry_name = tk.Entry(top); entry_name.grid(row=1, column=1)
        entry_qty = tk.Entry(top); entry_qty.grid(row=2, column=1)
        entry_price = tk.Entry(top); entry_price.grid(row=3, column=1)
        entry_batch = tk.Entry(top); entry_batch.grid(row=4, column=1)

        tk.Button(top, text="Save", command=save, bg="#00cec9", fg="white", width=15).grid(row=5, columnspan=2, pady=15)

    def process_sale(self):
        inventory = load_inventory()
        history = load_Sale()

        def process():
            ID = entry_id.get()
            city = entry_city.get()
            qty = entry_qty.get()

            if ID not in inventory:
                messagebox.showerror("Error", "Product ID not found!")
                return

            try:
                qty = int(qty)
            except ValueError:
                messagebox.showerror("Error", "Quantity must be integer!")
                return

            product = inventory[ID]
            if qty <= 0 or qty > product["Quantity"]:
                messagebox.showerror("Error", "Invalid quantity!")
                return

            product["Quantity"] -= qty
            total = qty * product["Price"]
            dump_inventory(inventory)

            invoice_id = ''.join(random.choices(string.ascii_letters, k=4))
            history[invoice_id] = {
                "ID": ID,
                "City": city,
                "Name": product["Name"],
                "Quantity": qty,
                "Unit_Price": product["Price"],
                "Total_Price": total,
                "Date": time.strftime("%d-%B-%Y"),
                "Time": str(datetime.now().time())
            }
            dump_Sale(history)

            messagebox.showinfo("Sale Processed", f"Sold {qty} units of {product['Name']} for Rs{total}")
            top.destroy()

        top = tk.Toplevel(self.root)
        top.title("Process Sale")
        top.geometry("350x250")
        top.configure(bg="#ffeaa7")

        tk.Label(top, text="Product ID:", bg="#ffeaa7").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        entry_id = tk.Entry(top); entry_id.grid(row=0, column=1)

        tk.Label(top, text="City:", bg="#ffeaa7").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        entry_city = tk.Entry(top); entry_city.grid(row=1, column=1)

        tk.Label(top, text="Quantity:", bg="#ffeaa7").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        entry_qty = tk.Entry(top); entry_qty.grid(row=2, column=1)

        tk.Button(top, text="Process", command=process, bg="#e17055", fg="white", width=15).grid(row=3, columnspan=2, pady=20)

    def update_stock(self):
        inventory = load_inventory()

        def update():
            ID = entry_id.get()
            qty = entry_qty.get()
            if ID not in inventory:
                messagebox.showerror("Error", "Product ID not found!")
                return
            try:
                qty = int(qty)
            except ValueError:
                messagebox.showerror("Error", "Quantity must be integer!")
                return
            inventory[ID]["Quantity"] += qty
            dump_inventory(inventory)
            messagebox.showinfo("Success", f"Updated stock. New Quantity: {inventory[ID]['Quantity']}")
            top.destroy()

        top = tk.Toplevel(self.root)
        top.title("Update Stock")
        top.geometry("350x200")
        top.configure(bg="#fab1a0")

        tk.Label(top, text="Product ID:", bg="#fab1a0").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        entry_id = tk.Entry(top); entry_id.grid(row=0, column=1)

        tk.Label(top, text="Quantity (+/-):", bg="#fab1a0").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        entry_qty = tk.Entry(top); entry_qty.grid(row=1, column=1)

        tk.Button(top, text="Update", command=update, bg="#d63031", fg="white", width=15).grid(row=2, columnspan=2, pady=20)

    def view_inventory(self):
        data = load_inventory()
        if not data:
            self.print_output("⚠️ No items in inventory.\n")
            return
        output = "Current Inventory:\n" + "-" * 30 + "\n"
        for ID, d in data.items():
            total = d["Quantity"] * d["Price"]
            output += f"ID: {ID}\nName: {d['Name']}\nQuantity: {d['Quantity']}\nPrice: Rs{d['Price']}\nTotal: Rs{total}\nBatch No: {d['Batch_No']}\n{'-'*30}\n"
        self.print_output(output)

    def view_history(self):
        data = load_Sale()
        if not data:
            self.print_output("⚠️ No sales history available.\n")
            return
        output = "Sales History:\n" + "-" * 30 + "\n"
        for ID, d in data.items():
            output += f"City: {d['City']}\nName: {d['Name']}\nQty: {d['Quantity']}\nPrice: Rs{d['Unit_Price']}\nTotal: Rs{d['Total_Price']}\nDate: {d['Date']} Time: {d['Time']}\n{'-'*30}\n"
        self.print_output(output)

    def delete_inventory(self):
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete all inventory?"):
            with open(INVENTORYFILE, 'w') as f:
                json.dump({}, f)
            self.print_output("Inventory cleared successfully.")

root = tk.Tk()
app = InventoryApp(root)
root.mainloop()
 