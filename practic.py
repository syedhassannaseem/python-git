import json
import os
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from tkinter.font import Font

INVENTORYFILE = "inventory.json"

class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System")
        self.root.geometry("900x650")
        self.root.configure(bg="#2c3e50")
        self.root.resizable(True, True)
        
        # Custom color scheme
        self.colors = {
            'bg': "#2c3e50",
            'header': "#3498db",
            'button': "#1abc9c",
            'button_hover': "#16a085",
            'exit_button': "#e74c3c",
            'exit_hover': "#c0392b",
            'tree_heading': "#2980b9",
            'tree_even': "#ecf0f1",
            'tree_odd': "#bdc3c7",
            'status': "#7f8c8d",
            'form_bg': "#34495e",
            'text': "#ecf0f1"
        }
        
        # Create custom fonts
        self.title_font = Font(family="Helvetica", size=18, weight="bold")
        self.button_font = Font(family="Arial", size=12, weight="bold")
        self.label_font = Font(family="Arial", size=11)
        self.status_font = Font(family="Arial", size=10)
        
        self.create_widgets()
        self.load_inventory()

    def create_widgets(self):
        # Header frame
        header_frame = tk.Frame(self.root, bg=self.colors['header'])
        header_frame.pack(fill="x", padx=10, pady=(10, 0))
        
        tk.Label(header_frame, text="Inventory Management System", 
                font=self.title_font, bg=self.colors['header'], fg="white").pack(pady=15)
        
        # Button frame
        button_frame = tk.Frame(self.root, bg=self.colors['bg'])
        button_frame.pack(fill="x", padx=20, pady=15)
        
        # Create buttons with hover effects
        add_btn = tk.Button(button_frame, text="➕ Add Product", font=self.button_font,
                          command=self.add_inventory, bg=self.colors['button'], fg="white",
                          activebackground=self.colors['button_hover'], activeforeground="white",
                          relief="flat", bd=0, padx=15, pady=8)
        add_btn.pack(side="left", padx=10)
        add_btn.bind("<Enter>", lambda e: add_btn.config(bg=self.colors['button_hover']))
        add_btn.bind("<Leave>", lambda e: add_btn.config(bg=self.colors['button']))
        
        view_btn = tk.Button(button_frame, text="👁️ View Inventory", font=self.button_font,
                           command=self.view_inventory, bg=self.colors['button'], fg="white",
                           activebackground=self.colors['button_hover'], activeforeground="white",
                           relief="flat", bd=0, padx=15, pady=8)
        view_btn.pack(side="left", padx=10)
        view_btn.bind("<Enter>", lambda e: view_btn.config(bg=self.colors['button_hover']))
        view_btn.bind("<Leave>", lambda e: view_btn.config(bg=self.colors['button']))
        
        exit_btn = tk.Button(button_frame, text="🚪 Exit", font=self.button_font,
                           command=self.root.destroy, bg=self.colors['exit_button'], fg="white",
                           activebackground=self.colors['exit_hover'], activeforeground="white",
                           relief="flat", bd=0, padx=15, pady=8)
        exit_btn.pack(side="right", padx=10)
        exit_btn.bind("<Enter>", lambda e: exit_btn.config(bg=self.colors['exit_hover']))
        exit_btn.bind("<Leave>", lambda e: exit_btn.config(bg=self.colors['exit_button']))
        
        # Treeview frame
        tree_frame = tk.Frame(self.root, bg=self.colors['bg'])
        tree_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Create treeview with styles
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"), 
                       background=self.colors['tree_heading'], foreground="white")
        style.configure("Treeview", font=("Arial", 11), rowheight=30)
        style.map("Treeview", background=[('selected', '#3498db')])
        
        self.tree = ttk.Treeview(tree_frame, columns=("ID", "Name", "Quantity", "Price", "BatchNo"), show="headings")
        
        # Define columns
        self.tree.heading("ID", text="Product ID", anchor="w")
        self.tree.heading("Name", text="Product Name", anchor="w")
        self.tree.heading("Quantity", text="Quantity", anchor="center")
        self.tree.heading("Price", text="Price (₹)", anchor="center")
        self.tree.heading("BatchNo", text="Batch No", anchor="w")
        
        # Set column widths
        self.tree.column("ID", width=150, anchor="w")
        self.tree.column("Name", width=250, anchor="w")
        self.tree.column("Quantity", width=100, anchor="center")
        self.tree.column("Price", width=150, anchor="center")
        self.tree.column("BatchNo", width=200, anchor="w")
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)
        
        # Status bar
        self.status = tk.Label(self.root, text="Ready", font=self.status_font, 
                             bg=self.colors['status'], fg="white", relief="sunken", anchor="w")
        self.status.pack(side="bottom", fill="x")

    def load_inventory(self):
        if os.path.exists(INVENTORYFILE):
            try:
                with open(INVENTORYFILE, "r") as h:
                    self.inventory = json.load(h)
                    self.update_treeview()
                    self.status.config(text=f"Loaded {len(self.inventory)} products")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load inventory: {str(e)}")
                self.inventory = {}
        else:
            self.inventory = {}
            self.status.config(text="No inventory found - created new")

    def dump_inventory(self):
        try:
            with open(INVENTORYFILE, "w") as g:
                json.dump(self.inventory, g, indent=4)
            self.status.config(text="Inventory saved successfully")
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save inventory: {str(e)}")
            return False

    def update_treeview(self):
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Add new data with alternating colors
        for i, (item_id, details) in enumerate(self.inventory.items()):
            tags = ('evenrow',) if i % 2 == 0 else ('oddrow',)
            self.tree.insert("", "end", values=(
                details["ID"],
                details["Name"],
                details["Quantity"],
                f'₹{details["Price"]:.2f}',
                details["Batch_No"]
            ), tags=tags)
        
        # Configure tag colors
        self.tree.tag_configure('evenrow', background=self.colors['tree_even'])
        self.tree.tag_configure('oddrow', background=self.colors['tree_odd'])

    def add_inventory(self):
        # Create add product window
        add_window = tk.Toplevel(self.root)
        add_window.title("Add New Product")
        add_window.geometry("500x400")
        add_window.resizable(False, False)
        add_window.configure(bg=self.colors['form_bg'])
        add_window.grab_set()
        
        # Header
        tk.Label(add_window, text="Add New Product", font=self.title_font, 
                bg=self.colors['header'], fg="white").pack(fill="x", pady=(0, 15))
        
        # Form frame
        form_frame = tk.Frame(add_window, bg=self.colors['form_bg'])
        form_frame.pack(padx=30, pady=10, fill="both", expand=True)
        
        # Form fields with colorful labels
        tk.Label(form_frame, text="Product ID:", font=self.label_font, 
                bg=self.colors['form_bg'], fg=self.colors['text']).grid(row=0, column=0, padx=5, pady=10, sticky="e")
        id_entry = tk.Entry(form_frame, font=self.label_font, width=30)
        id_entry.grid(row=0, column=1, padx=5, pady=10, sticky="w")
        id_entry.focus()
        
        tk.Label(form_frame, text="Product Name:", font=self.label_font, 
                bg=self.colors['form_bg'], fg=self.colors['text']).grid(row=1, column=0, padx=5, pady=10, sticky="e")
        name_entry = tk.Entry(form_frame, font=self.label_font, width=30)
        name_entry.grid(row=1, column=1, padx=5, pady=10, sticky="w")
        
        tk.Label(form_frame, text="Quantity:", font=self.label_font, 
                bg=self.colors['form_bg'], fg=self.colors['text']).grid(row=2, column=0, padx=5, pady=10, sticky="e")
        qty_entry = tk.Entry(form_frame, font=self.label_font, width=30)
        qty_entry.grid(row=2, column=1, padx=5, pady=10, sticky="w")
        
        tk.Label(form_frame, text="Price (₹):", font=self.label_font, 
                bg=self.colors['form_bg'], fg=self.colors['text']).grid(row=3, column=0, padx=5, pady=10, sticky="e")
        price_entry = tk.Entry(form_frame, font=self.label_font, width=30)
        price_entry.grid(row=3, column=1, padx=5, pady=10, sticky="w")
        
        tk.Label(form_frame, text="Batch No:", font=self.label_font, 
                bg=self.colors['form_bg'], fg=self.colors['text']).grid(row=4, column=0, padx=5, pady=10, sticky="e")
        batch_entry = tk.Entry(form_frame, font=self.label_font, width=30)
        batch_entry.grid(row=4, column=1, padx=5, pady=10, sticky="w")
        
        # Button frame
        button_frame = tk.Frame(add_window, bg=self.colors['form_bg'])
        button_frame.pack(pady=10)
        
        # Submit button with hover effect
        submit_btn = tk.Button(button_frame, text="Save Product", font=self.button_font,
                             command=lambda: self.save_product(
                                 id_entry.get(),
                                 name_entry.get(),
                                 qty_entry.get(),
                                 price_entry.get(),
                                 batch_entry.get(),
                                 add_window
                             ), bg=self.colors['button'], fg="white",
                             activebackground=self.colors['button_hover'], activeforeground="white",
                             relief="flat", bd=0, padx=15, pady=8)
        submit_btn.pack(side="left", padx=10)
        submit_btn.bind("<Enter>", lambda e: submit_btn.config(bg=self.colors['button_hover']))
        submit_btn.bind("<Leave>", lambda e: submit_btn.config(bg=self.colors['button']))
        
        # Cancel button with hover effect
        cancel_btn = tk.Button(button_frame, text="Cancel", font=self.button_font,
                             command=add_window.destroy, bg=self.colors['exit_button'], fg="white",
                             activebackground=self.colors['exit_hover'], activeforeground="white",
                             relief="flat", bd=0, padx=15, pady=8)
        cancel_btn.pack(side="left", padx=10)
        cancel_btn.bind("<Enter>", lambda e: cancel_btn.config(bg=self.colors['exit_hover']))
        cancel_btn.bind("<Leave>", lambda e: cancel_btn.config(bg=self.colors['exit_button']))

    def save_product(self, prod_id, name, qty, price, batch, window):
        # Validate inputs
        if not prod_id:
            messagebox.showerror("Error", "Product ID cannot be empty!")
            return
            
        if prod_id in self.inventory:
            messagebox.showerror("Error", f"Product ID '{prod_id}' already exists!")
            return
            
        if not name:
            messagebox.showerror("Error", "Product name cannot be empty!")
            return
            
        try:
            qty = int(qty)
            if qty < 0:
                raise ValueError("Quantity must be positive")
        except ValueError:
            messagebox.showerror("Error", "Quantity must be a positive integer!")
            return
            
        try:
            price = float(price)
            if price <= 0:
                raise ValueError("Price must be positive")
        except ValueError:
            messagebox.showerror("Error", "Price must be a positive number!")
            return
            
        if not batch:
            messagebox.showerror("Error", "Batch number cannot be empty!")
            return
            
        # Add to inventory
        self.inventory[prod_id] = {
            "ID": prod_id,
            "Name": name,
            "Quantity": qty,
            "Price": price,
            "Batch_No": batch
        }
        
        # Save and update
        if self.dump_inventory():
            self.update_treeview()
            messagebox.showinfo("Success", "Product added successfully!")
            window.destroy()

    def view_inventory(self):
        if not self.inventory:
            messagebox.showinfo("Inventory", "No items in inventory")
            return
            
        # Create view window
        view_window = tk.Toplevel(self.root)
        view_window.title("View Inventory")
        view_window.geometry("800x500")
        view_window.configure(bg=self.colors['bg'])
        
        # Header
        tk.Label(view_window, text="Current Inventory", font=self.title_font, 
                bg=self.colors['header'], fg="white").pack(fill="x", pady=(0, 15))
        
        # Treeview frame
        tree_frame = tk.Frame(view_window, bg=self.colors['bg'])
        tree_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Create treeview with styles
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"), 
                       background=self.colors['tree_heading'], foreground="white")
        style.configure("Treeview", font=("Arial", 11), rowheight=30)
        
        tree = ttk.Treeview(tree_frame, columns=("ID", "Name", "Quantity", "Price", "BatchNo"), show="headings")
        
        # Define columns
        tree.heading("ID", text="Product ID", anchor="w")
        tree.heading("Name", text="Product Name", anchor="w")
        tree.heading("Quantity", text="Quantity", anchor="center")
        tree.heading("Price", text="Price (₹)", anchor="center")
        tree.heading("BatchNo", text="Batch No", anchor="w")
        
        # Set column widths
        tree.column("ID", width=150, anchor="w")
        tree.column("Name", width=250, anchor="w")
        tree.column("Quantity", width=100, anchor="center")
        tree.column("Price", width=150, anchor="center")
        tree.column("BatchNo", width=200, anchor="w")
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        tree.pack(fill="both", expand=True)
        
        # Add data with alternating colors
        for i, (item_id, details) in enumerate(self.inventory.items()):
            tags = ('evenrow',) if i % 2 == 0 else ('oddrow',)
            tree.insert("", "end", values=(
                details["ID"],
                details["Name"],
                details["Quantity"],
                f'₹{details["Price"]:.2f}',
                details["Batch_No"]
            ), tags=tags)
        
        # Configure tag colors
        tree.tag_configure('evenrow', background=self.colors['tree_even'])
        tree.tag_configure('oddrow', background=self.colors['tree_odd'])
        
        # Status label
        tk.Label(view_window, text=f"Total Products: {len(self.inventory)}", 
                font=("Arial", 12, "bold"), bg=self.colors['bg'], fg=self.colors['text']).pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryApp(root)
    root.mainloop()