import json
import os
import csv
from datetime import datetime
from uuid import uuid4
import getpass

class AdvancedInventorySystem:
    def __init__(self):
        self.products_file = "products.json"
        self.sales_file = "sales.json"
        self.users_file = "users.json"
        self.suppliers_file = "suppliers.json"
        self.backup_dir = "backups"
        
        # Create backup directory if not exists
        os.makedirs(self.backup_dir, exist_ok=True)
        
        self.products = self.load_data(self.products_file)
        self.sales = self.load_data(self.sales_file)
        self.users = self.load_data(self.users_file)
        self.suppliers = self.load_data(self.suppliers_file)
        
        # Default admin user if no users exist
        if not self.users:
            self.users["admin"] = {
                "password": "admin123",
                "role": "admin",
                "full_name": "System Administrator"
            }
            self.save_data(self.users, self.users_file)

    # === Core Functions ===
    def load_data(self, filename):
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                return json.load(file)
        return {}

    def save_data(self, data, filename):
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)

    def generate_id(self, prefix):
        return f"{prefix}_{str(uuid4())[:8]}"

    # === Authentication ===
    # def login(self):
    #     print("\n=== Login ===")
    #     username = input("Username: ")
    #     password = getpass.getpass("Password: ")
        
    #     if username in self.users and self.users[username]["password"] == password:
    #         self.current_user = username
    #         self.user_role = self.users[username]["role"]
    #         print(f"\nWelcome, {self.users[username]['full_name']} ({self.user_role})!")
    #         return True
    #     print("Invalid username or password!")
    #     return False

    # === Advanced Product Management ===
    def add_product(self):
        if self.user_role not in ["admin", "manager"]:
            print("Permission denied!")
            return
            
        print("\n--- Add New Product ---")
        product_id = self.generate_id("PROD")
        name = input("Enter product name: ")
        price = float(input("Enter product price: "))
        quantity = int(input("Enter initial quantity: "))
        category = input("Enter product category: ")
        supplier_id = input("Enter supplier ID (leave blank if none): ")
        
        if supplier_id and supplier_id not in self.suppliers:
            print("Supplier not found!")
            return
            
        self.products[product_id] = {
            'name': name,
            'price': price,
            'quantity': quantity,
            'category': category,
            'supplier': supplier_id if supplier_id else None,
            'reorder_level': int(input("Enter reorder level: ") or "5"),
            'date_added': str(datetime.now()),
            'last_updated': str(datetime.now())
        }
        self.save_data(self.products, self.products_file)
        print(f"Product added successfully! ID: {product_id}")

    def search_products(self):
        print("\n--- Search Products ---")
        search_term = input("Enter product name or ID to search: ").lower()
        
        found = False
        for pid, product in self.products.items():
            if (search_term in pid.lower() or 
                search_term in product['name'].lower()):
                found = True
                print(f"\nID: {pid}")
                print(f"Name: {product['name']}")
                print(f"Price: ${product['price']:.2f}")
                print(f"Stock: {product['quantity']}")
                print(f"Category: {product['category']}")
                
        if not found:
            print("No products found matching your search.")

    # === Supplier Management ===
    def add_supplier(self):
        if self.user_role != "admin":
            print("Permission denied!")
            return
            
        print("\n--- Add New Supplier ---")
        supplier_id = self.generate_id("SUPP")
        name = input("Supplier name: ")
        contact = input("Contact person: ")
        phone = input("Phone number: ")
        email = input("Email: ")
        products = input("Products supplied (comma separated): ").split(',')
        
        self.suppliers[supplier_id] = {
            'name': name,
            'contact': contact,
            'phone': phone,
            'email': email,
            'products': [p.strip() for p in products],
            'date_added': str(datetime.now())
        }
        self.save_data(self.suppliers, self.suppliers_file)
        print(f"Supplier added successfully! ID: {supplier_id}")

    # === Advanced Reporting ===
    def generate_report(self):
        print("\n--- Generate Report ---")
        print("1. Inventory Summary")
        print("2. Sales Report")
        print("3. Low Stock Report")
        print("4. Category-wise Report")
        choice = input("Enter report type (1-4): ")
        
        report_date = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"report_{report_date}.csv"
        
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            
            if choice == '1':
                writer.writerow(["ID", "Name", "Category", "Price", "Quantity", "Value"])
                total_value = 0
                for pid, product in self.products.items():
                    value = product['price'] * product['quantity']
                    writer.writerow([
                        pid, product['name'], product['category'],
                        product['price'], product['quantity'], value
                    ])
                    total_value += value
                writer.writerow(["", "", "", "", "Total Value", total_value])
                print(f"Inventory summary report generated: {filename}")
                
            elif choice == '2':
                # Similar implementation for sales report
                pass
                
            # Implement other report types similarly

    # === Data Backup ===
    def backup_data(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(self.backup_dir, f"backup_{timestamp}.json")
        
        all_data = {
            'products': self.products,
            'sales': self.sales,
            'users': self.users,
            'suppliers': self.suppliers
        }
        
        with open(backup_file, 'w') as file:
            json.dump(all_data, file, indent=4)
            
        print(f"Backup created successfully: {backup_file}")

    # === User Management ===
    def add_user(self):
        if self.user_role != "admin":
            print("Permission denied!")
            return
            
        print("\n--- Add New User ---")
        username = input("Enter username: ")
        if username in self.users:
            print("Username already exists!")
            return
            
        full_name = input("Full name: ")
        password = getpass.getpass("Password: ")
        role = input("Role (admin/manager/staff): ")
        
        self.users[username] = {
            "password": password,
            "role": role,
            "full_name": full_name
        }
        self.save_data(self.users, self.users_file)
        print("User added successfully!")

    # === Barcode Simulation ===
    def barcode_scan(self):
        print("\n--- Barcode Scanner ---")
        print("Simulating barcode scanner...")
        barcode = input("Enter product ID or barcode: ")
        
        if barcode in self.products:
            product = self.products[barcode]
            print(f"\nProduct Found:")
            print(f"Name: {product['name']}")
            print(f"Price: ${product['price']:.2f}")
            print(f"Stock: {product['quantity']}")
            return barcode
        else:
            print("Product not found in inventory!")
            return None

    # === Main Menu ===
    def run(self):
        if not self.login():
            return
            
        while True:
            print("\n=== Advanced Inventory System ===")
            print(f"Logged in as: {self.current_user} ({self.user_role})")
            print("\n1. Product Management")
            print("2. Sales Processing")
            print("3. Supplier Management")
            print("4. Reports")
            print("5. User Management")
            print("6. System Utilities")
            print("7. Logout")
            
            choice = input("Enter your choice (1-7): ")
            
            if choice == '1':
                # Product management submenu
                pass
            elif choice == '2':
                # Sales processing submenu
                pass
            # Implement other menu options similarly
            elif choice == '7':
                print("Logging out...")
                break
            else:
                print("Invalid choice!")

if __name__ == "__main__":
    system = AdvancedInventorySystem()
    system.run()