import json
import os
from datetime import datetime

class InventorySystem:
    def __init__(self):
        self.products_file = "products.json"
        self.sales_file = "sales.json"
        self.products = self.load_data(self.products_file)
        self.sales = self.load_data(self.sales_file)

    def load_data(self, filename):
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                return json.load(file)
        return {}

    def save_data(self, data, filename):
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)

    def add_product(self):
        print("\n--- Add New Product ---")
        product_id = input("Enter product ID: ")
        if product_id in self.products:
            print("Product ID already exists!")
            return
            
        name = input("Enter product name: ")
        price = float(input("Enter product price: "))
        quantity = int(input("Enter initial quantity: "))
        category = input("Enter product category: ")
        
        self.products[product_id] = {
            'name': name,
            'price': price,
            'quantity': quantity,
            'category': category,
            'date_added': str(datetime.now())
        }
        self.save_data(self.products, self.products_file)
        print("Product added successfully!")

    def view_products(self):
        print("\n--- Product Inventory ---")
        if not self.products:
            print("No products in inventory.")
            return
            
        for product_id, details in self.products.items():
            print(f"\nID: {product_id}")
            print(f"Name: {details['name']}")
            print(f"Price: ${details['price']:.2f}")
            print(f"Quantity: {details['quantity']}")
            print(f"Category: {details['category']}")
            print(f"Added On: {details['date_added']}")

    def update_stock(self):
        print("\n--- Update Stock ---")
        product_id = input("Enter product ID to update: ")
        if product_id not in self.products:
            print("Product not found!")
            return
            
        print(f"\nCurrent stock: {self.products[product_id]['quantity']}")
        change = int(input("Enter quantity to add/subtract (use - for subtraction): "))
        self.products[product_id]['quantity'] += change
        self.save_data(self.products, self.products_file)
        print(f"Stock updated. New quantity: {self.products[product_id]['quantity']}")
        

    def process_sale(self):
        print("\n--- Process Sale ---")
        product_id = input("Enter product ID: ")
        if product_id not in self.products:
            print("Product not found!")
            return
            
        available = self.products[product_id]['quantity']
        if available <= 0:
            print("Product out of stock!")
            return
            
        print(f"Available: {available}")
        quantity = int(input("Enter quantity to sell: "))
        
        if quantity > available:
            print("Not enough stock!")
            return
            
        self.products[product_id]['quantity'] -= quantity
        sale_id = str(len(self.sales) + 1)
        
        self.sales[sale_id] = {
            'product_id': product_id,
            'product_name': self.products[product_id]['name'],
            'quantity': quantity,
            'unit_price': self.products[product_id]['price'],
            'total': quantity * self.products[product_id]['price'],
            'date': str(datetime.now())
        }
        
        self.save_data(self.products, self.products_file)
        self.save_data(self.sales, self.sales_file)
        
        print("\n--- Receipt ---")
        print(f"Product: {self.products[product_id]['name']}")
        print(f"Quantity: {quantity}")
        print(f"Unit Price: ${self.products[product_id]['price']:.2f}")
        print(f"Total: ${quantity * self.products[product_id]['price']:.2f}")
        print("Sale completed successfully!")

    def view_sales(self):
        print("\n--- Sales History ---")
        if not self.sales:
            print("No sales recorded.")
            return
            
        for sale_id, details in self.sales.items():
            print(f"\nSale ID: {sale_id}")
            print(f"Product: {details['product_name']} ({details['product_id']})")
            print(f"Quantity: {details['quantity']}")
            print(f"Unit Price: ${details['unit_price']:.2f}")
            print(f"Total: ${details['total']:.2f}")
            print(f"Date: {details['date']}")

    def check_low_stock(self, threshold=5):
        print("\n--- Low Stock Alert ---")
        low_stock = False
        
        for product_id, details in self.products.items():
            if details['quantity'] <= threshold:
                low_stock = True
                print(f"{details['name']} (ID: {product_id}) - Only {details['quantity']} left!")
        
        if not low_stock:
            print("No products are low in stock.")

    def run(self):
        while True:
            print("\n=== Inventory Management System ===")
            print("1. Add New Product")
            print("2. View All Products")
            print("3. Update Stock")
            print("4. Process Sale")
            print("5. View Sales History")
            print("6. Check Low Stock")
            print("7. Exit")
            
            choice = input("Enter your choice (1-7): ")
            
            if choice == '1':
                self.add_product()
            elif choice == '2':
                self.view_products()
            elif choice == '3':
                self.update_stock()
            elif choice == '4':
                self.process_sale()
            elif choice == '5':
                self.view_sales()
            elif choice == '6':
                self.check_low_stock()
            elif choice == '7':
                print("Exiting the system. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    system = InventorySystem()
    system.run()