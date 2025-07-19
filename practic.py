import json
import os
import win10toast
import time
from datetime import datetime
import random
import string
import tkinter as tk
from tkinter import ttk, messagebox

INVENTORYFILE = "inventory.json"
HISTORY = "Sales_History.json"

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

def Notification():
    data = load_inventory()
    to = win10toast.ToastNotifier()
    for ID, details in data.items():
        if details["Quantity"] <= 500:
            to.show_toast(
                "⚠️ WARNING",
                f"➡️ {details['Name']} is running low (Only {details['Quantity']} left!)",
                duration=3,
                threaded=True
            )
            time.sleep(3.4)

class InventoryApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Inventory Management System")
        self.geometry("800x600")
        self.configure(bg="#f0f0f0")
        self.create_widgets()
        Notification()

    def create_widgets(self):
        self.main_menu()

    def main_menu(self):
        for widget in self.winfo_children():
            widget.destroy()

        tk.Label(self, text="Inventory Management System", font=("Arial", 20, "bold"), bg="#f0f0f0").pack(pady=20)

        buttons = [
            ("Add Product", self.add_inventory_ui),
            ("Process Sale", self.process_sale_ui),
            ("Update Stock", self.update_stock_ui),
            ("View Inventory", self.view_inventory_ui),
            ("View Sales History", self.view_history_ui),
            ("Delete Inventory", self.delete_inventory_ui),
            ("Exit", self.quit)
        ]

        for text, command in buttons:
            tk.Button(self, text=text, width=25, height=2, command=command, bg="#4CAF50", fg="white").pack(pady=10)

    def back_to_menu(self):
        self.main_menu()

    def add_inventory_ui(self):
        self.clear_widgets()

        tk.Label(self, text="Add New Product", font=("Arial", 16)).pack(pady=10)

        labels = ["Product ID", "Name", "Quantity", "Price", "Batch No"]
        entries = {}

        for label in labels:
            tk.Label(self, text=label).pack()
            entry = tk.Entry(self)
            entry.pack()
            entries[label] = entry

        def save():
            inventory = load_inventory()
            ID = entries["Product ID"].get()
            if ID in inventory:
                messagebox.showerror("Error", "Product ID already exists!")
                return
            try:
                inventory[ID] = {
                    "Name": entries["Name"].get(),
                    "Quantity": int(entries["Quantity"].get()),
                    "Price": float(entries["Price"].get()),
                    "Batch_No": entries["Batch No"].get()
                }
            except ValueError:
                messagebox.showerror("Error", "Quantity and Price must be numbers")
                return

            dump_inventory(inventory)
            messagebox.showinfo("Success", "Product added successfully")
            self.back_to_menu()

        tk.Button(self, text="Save", command=save, bg="#4CAF50", fg="white").pack(pady=10)
        tk.Button(self, text="Back", command=self.back_to_menu).pack()

    def view_inventory_ui(self):
        self.clear_widgets()

        tk.Label(self, text="Current Inventory", font=("Arial", 16)).pack(pady=10)

        tree = ttk.Treeview(self, columns=("ID", "Name", "Quantity", "Price", "Total", "Batch"), show="headings")
        for col in tree["columns"]:
            tree.heading(col, text=col)
            tree.column(col, anchor="center")
        tree.pack(fill="both", expand=True)

        data = load_inventory()
        for ID, d in data.items():
            total = d["Quantity"] * d["Price"]
            tree.insert('', 'end', values=(ID, d["Name"], d["Quantity"], d["Price"], total, d["Batch_No"]))

        tk.Button(self, text="Back", command=self.back_to_menu).pack(pady=10)

    def view_history_ui(self):
        self.clear_widgets()

        tk.Label(self, text="Sales History", font=("Arial", 16)).pack(pady=10)

        tree = ttk.Treeview(self, columns=("ID", "City", "Name", "Quantity", "Unit Price", "Total Price", "Date", "Time"), show="headings")
        for col in tree["columns"]:
            tree.heading(col, text=col)
            tree.column(col, anchor="center")
        tree.pack(fill="both", expand=True)

        data = load_Sale()
        for ID, d in data.items():
            if all(k in d for k in ["ID", "City", "Name", "Quantity", "Unit_Price", "Total_Price", "Date", "Time"]):
                tree.insert('', 'end', values=(d["ID"], d["City"], d["Name"], d["Quantity"], d["Unit_Price"], d["Total_Price"], d["Date"], d["Time"]))

        tk.Button(self, text="Back", command=self.back_to_menu).pack(pady=10)

    def process_sale_ui(self):
        self.clear_widgets()

        tk.Label(self, text="Process Sale", font=("Arial", 16)).pack(pady=10)
        tk.Label(self, text="Enter Product ID:").pack()
        product_entry = tk.Entry(self)
        product_entry.pack()

        tk.Label(self, text="Enter City:").pack()
        city_entry = tk.Entry(self)
        city_entry.pack()

        tk.Label(self, text="Enter Quantity:").pack()
        qty_entry = tk.Entry(self)
        qty_entry.pack()

        def sell():
            ID = product_entry.get()
            city = city_entry.get()
            try:
                qty = int(qty_entry.get())
            except ValueError:
                messagebox.showerror("Error", "Quantity must be an integer")
                return

            data = load_inventory()
            history = load_Sale()

            if ID in data:
                if qty > 0 and data[ID]["Quantity"] >= qty:
                    data[ID]["Quantity"] -= qty
                    total = qty * data[ID]["Price"]
                    dump_inventory(data)

                    invoice = ''.join(random.choices(string.ascii_letters, k=4))
                    history[invoice] = {
                        "ID": ID,
                        "City": city,
                        "Name": data[ID]["Name"],
                        "Quantity": qty,
                        "Unit_Price": data[ID]["Price"],
                        "Total_Price": total,
                        "Date": time.strftime("%d-%B-%Y"),
                        "Time": str(datetime.now().time())
                    }
                    dump_Sale(history)
                    messagebox.showinfo("Success", "Sale processed successfully")
                    self.back_to_menu()
                else:
                    messagebox.showerror("Error", "Invalid quantity")
            else:
                messagebox.showerror("Error", "Product ID not found")

        tk.Button(self, text="Sell", command=sell, bg="#4CAF50", fg="white").pack(pady=10)
        tk.Button(self, text="Back", command=self.back_to_menu).pack()

    def update_stock_ui(self):
        self.clear_widgets()

        tk.Label(self, text="Update Stock", font=("Arial", 16)).pack(pady=10)

        tk.Label(self, text="Enter Product ID:").pack()
        id_entry = tk.Entry(self)
        id_entry.pack()

        tk.Label(self, text="Enter Quantity (+/-):").pack()
        qty_entry = tk.Entry(self)
        qty_entry.pack()

        def update():
            ID = id_entry.get()
            try:
                change = int(qty_entry.get())
            except ValueError:
                messagebox.showerror("Error", "Enter valid number")
                return

            data = load_inventory()
            if ID in data:
                data[ID]["Quantity"] += change
                dump_inventory(data)
                messagebox.showinfo("Success", f"New Quantity: {data[ID]['Quantity']}")
                self.back_to_menu()
            else:
                messagebox.showerror("Error", "Product ID not found")

        tk.Button(self, text="Update", command=update, bg="#4CAF50", fg="white").pack(pady=10)
        tk.Button(self, text="Back", command=self.back_to_menu).pack()

    def delete_inventory_ui(self):
        if messagebox.askyesno("Warning", "Are you sure you want to delete all inventory data?"):
            with open(INVENTORYFILE, 'w') as file:
                json.dump({}, file)
            messagebox.showinfo("Deleted", "Inventory cleared successfully")

    def clear_widgets(self):
        for widget in self.winfo_children():
            widget.destroy()

if __name__ == '__main__':
    app = InventoryApp()
    app.mainloop()
