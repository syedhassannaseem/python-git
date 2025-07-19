import json 
import os
import time
from datetime import datetime
from colorama import init, Fore, Back, Style

# Initialize colorama
init(autoreset=True)

INVENTORYFILE = "inventory.json"
HISTORY = "Sales_History.json"

# UI Design Elements
def print_header(title):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Fore.YELLOW + "=" * 80)
    print(Fore.CYAN + f"{title:^80}")
    print(Fore.YELLOW + "=" * 80 + "\n")

def print_menu():
    print(Fore.GREEN + "\n" + "=" * 30 + " MENU " + "=" * 30)
    print(Fore.CYAN + "1. Add Product")
    print("2. Process Sale")
    print("3. Update Stock")
    print("4. View Inventory")
    print("5. View Sales History")
    print("6. Clear Inventory")
    print("7. Exit")
    print(Fore.GREEN + "=" * 66 + "\n")

def print_success(message):
    print(Fore.GREEN + f"\n✓ {message}\n")

def print_error(message):
    print(Fore.RED + f"\n⚠ {message}\n")

def print_warning(message):
    print(Fore.YELLOW + f"\n! {message}\n")

def print_table_header(headers):
    print(Fore.BLUE + "+" + "-" * 78 + "+")
    header_line = "|"
    for header in headers:
        header_line += f" {header:^15} |"
    print(Fore.BLUE + header_line)
    print("+" + "-" * 78 + "+")

def print_table_row(items):
    row = "|"
    for item in items:
        row += f" {str(item):^15} |"
    print(row)
    print("+" + "-" * 78 + "+")

# Core Functions
def dump_inventory(inventory):
    with open(INVENTORYFILE, "w") as g:
        json.dump(inventory, g, indent=4)

def load_inventory():
    if os.path.exists(INVENTORYFILE):
        try:
            with open(INVENTORYFILE, "r") as h:
                return json.load(h)
        except json.JSONDecodeError:
            print_error("Inventory file is corrupted. Creating new inventory.")
            return {}
    else:
        print_error("Inventory Not Found! Creating new inventory.")
    return {}

def dump_Sale(sale):
    with open(HISTORY, "w") as g:
        json.dump(sale, g, indent=4)

def load_Sale():
    if os.path.exists(HISTORY):
        try:
            with open(HISTORY, "r") as h:
                return json.load(h)
        except json.JSONDecodeError:
            print_error("Sales history file is corrupted. Creating new history.")
            return {}
    else:
        print_error("Sales History Not Found! Creating new history.")
    return {}

# Inventory Operations
def add_inventory():
    print_header("ADD NEW PRODUCT")
    inventory = load_inventory()
    
    while True:
        ID = input(Fore.WHITE + "Enter Product ID (or 'back' to return): ").strip()
        if ID.lower() == 'back':
            return
        
        if not ID:
            print_error("Product ID cannot be empty!")
            continue
            
        if ID in inventory:
            print_error(f"Product ID '{ID}' already exists!")
            continue
            
        try:
            Name = input("Enter Product Name: ").strip()
            if not Name:
                print_error("Product name cannot be empty!")
                continue
                
            Quantity = int(input("Enter Product Quantity: "))
            if Quantity < 0:
                print_error("Quantity cannot be negative!")
                continue
                
            Price = float(input("Enter Product Price: "))
            if Price <= 0:
                print_error("Price must be positive!")
                continue
                
            Batch_No = input("Enter Product Batch No: ").strip()
            if not Batch_No:
                print_error("Batch number cannot be empty!")
                continue
                
            inventory[ID] = {
                "Name": Name,
                "Quantity": Quantity,
                "Price": Price,
                "Batch_No": Batch_No 
            }
            dump_inventory(inventory)
            print_success("Product details saved successfully!")
            time.sleep(1)
            break
            
        except ValueError as e:
            print_error(f"Invalid input: {e}")

def view_inventory():
    print_header("CURRENT INVENTORY")
    data = load_inventory()
    
    if not data:
        print_warning("No items in inventory")
        return
    
    headers = ["ID", "Name", "Quantity", "Price", "Batch No", "Total Value"]
    print_table_header(headers)
    
    for item_id, details in data.items():
        total_value = details["Quantity"] * details["Price"]
        print_table_row([
            item_id,
            details['Name'],
            details['Quantity'],
            f"Rs{details['Price']:.2f}",
            details['Batch_No'],
            f"Rs{total_value:.2f}"
        ])

def update_stock():
    print_header("UPDATE STOCK")
    data = load_inventory()
    
    if not data:
        print_warning("No items in inventory to update")
        return
    
    view_inventory()
    print("\n")
    
    while True:
        id = input("Enter Product ID to update (or 'back' to return): ").strip()
        if id.lower() == 'back':
            return
            
        if id not in data:
            print_error("Product not found!")
            continue
            
        details = data[id]
        print(Fore.CYAN + f"\nCurrent details for {details['Name']}:")
        print(f"Quantity: {details['Quantity']}")
        print(f"Price: Rs{details['Price']:.2f}\n")
        
        try:
            change = input("Enter quantity to add/subtract (use - for subtraction): ")
            if not change:
                print_error("Quantity change cannot be empty!")
                continue
                
            change = int(change)
            details["Quantity"] += change
            if details["Quantity"] < 0:
                details["Quantity"] = 0
                print_warning("Quantity cannot be negative. Set to 0.")
                
            new_price = input("Enter new price (leave blank to keep current): ")
            if new_price:
                new_price = float(new_price)
                if new_price <= 0:
                    print_error("Price must be positive!")
                    continue
                details["Price"] = new_price
                
            dump_inventory(data)
            print_success(f"Updated successfully! New quantity: {details['Quantity']}")
            time.sleep(1)
            break
            
        except ValueError as e:
            print_error(f"Invalid input: {e}")

def delete_inventory():
    print_header("CLEAR INVENTORY")
    confirm = input(Fore.RED + "Are you sure you want to clear ALL inventory data? (yes/no): ").lower()
    if confirm == 'yes':
        with open(INVENTORYFILE, 'w') as file:
            json.dump({}, file)
        print_success("Inventory cleared successfully!")
    else:
        print_success("Operation cancelled.")
    time.sleep(1)

# Sales Operations
def process_sale():
    print_header("PROCESS SALE")
    data = load_inventory()
    
    if not data:
        print_warning("No items in inventory to sell")
        time.sleep(1)
        return
    
    view_inventory()
    print("\n")
    history = load_Sale()
    sale_items = []
    total_sale = 0
    
    while True:
        product_id = input("\nEnter product ID (or 'done' to finish): ").strip()
        if product_id.lower() == 'done':
            break
            
        if product_id not in data:
            print_error("Product not found!")
            continue
            
        details = data[product_id]
        print(Fore.CYAN + f"\nProduct: {details['Name']}")
        print(f"Available Quantity: {details['Quantity']}")
        print(f"Price: Rs{details['Price']:.2f}\n")
        
        try:
            city = input("Enter customer city: ").strip()
            if not city:
                print_error("City cannot be empty!")
                continue
                
            quantity = input("Enter quantity to sell: ")
            if not quantity:
                print_error("Quantity cannot be empty!")
                continue
                
            quantity = int(quantity)
            
            if quantity <= 0:
                print_error("Quantity must be positive!")
                continue
                
            if quantity > details['Quantity']:
                print_error(f"Insufficient stock! Only {details['Quantity']} available.")
                continue
                
            details["Quantity"] -= quantity
            item_total = quantity * details["Price"]
            total_sale += item_total
            
            # Add to sale items
            sale_items.append({
                "name": details["Name"],
                "quantity": quantity,
                "price": details["Price"],
                "total": item_total
            })
            
            # Save to history
            timestamp = datetime.now()
            sale_id = f"{timestamp.strftime('%Y%m%d%H%M%S')}_{product_id}"
            
            history[sale_id] = {
                "ID": product_id,
                "City": city,
                "Name": details["Name"],
                "Quantity": quantity,
                "Unit_Price": details["Price"],
                "Total_Price": item_total,
                "Date": timestamp.strftime("%d-%B-%Y"),
                "Time": timestamp.strftime("%H:%M:%S")
            }
            
            print_success(f"Added {quantity} x {details['Name']} to sale (Rs{item_total:.2f})")
            
        except ValueError as e:
            print_error(f"Invalid input: {e}")
    
    if sale_items:
        # Update inventory
        dump_inventory(data)
        dump_Sale(history)
        
        # Print receipt
        print_header("SALE RECEIPT")
        print(Fore.CYAN + f"{'Product':<20} {'Qty':>5} {'Price':>10} {'Total':>10}")
        print("-" * 50)
        for item in sale_items:
            print(f"{item['name']:<20} {item['quantity']:>5} {f'Rs{item['price']:.2f}':>10} {f'Rs{item['total']:.2f}':>10}")
        print("-" * 50)
        print(Fore.GREEN + f"{'TOTAL:':<20} {'':>5} {'':>10} {f'Rs{total_sale:.2f}':>10}")
        print("\n")
        
        print_success("Sale processed successfully!")
    else:
        print_warning("No items were sold.")
    
    input("\nPress Enter to continue...")

def view_history():
    print_header("SALES HISTORY")
    data = load_Sale()
    
    if not data:
        print_warning("No sales history available")
        time.sleep(1)
        return
    
    headers = ["Date", "Time", "Product ID", "Name", "Qty", "Unit Price", "Total", "City"]
    print_table_header(headers)
    
    # Sort by date and time (newest first)
    sorted_sales = sorted(data.items(), key=lambda x: (x[1]['Date'], x[1]['Time']), reverse=True)
    
    for sale_id, details in sorted_sales:
        print_table_row([
            details['Date'],
            details['Time'],
            details['ID'],
            details['Name'],
            details['Quantity'],
            f"Rs{details['Unit_Price']:.2f}",
            f"Rs{details['Total_Price']:.2f}",
            details['City']
        ])
    
    input("\nPress Enter to continue...")

# Notification System
def check_low_stock():
    data = load_inventory()
    low_stock_items = []
    
    for ID, details in data.items():
        if details["Quantity"] <= 500:
            low_stock_items.append((details['Name'], details['Quantity']))
    
    if low_stock_items:
        print_header("LOW STOCK ALERT")
        print(Fore.RED + "The following products are running low:")
        for name, qty in low_stock_items:
            print(f"• {name}: only {qty} remaining")
        
        # Try to show notification (Windows only)
        try:
            from win10toast import ToastNotifier
            toaster = ToastNotifier()
            toaster.show_toast(
                "Inventory Alert",
                f"{len(low_stock_items)} product(s) running low!",
                duration=5,
                threaded=True
            )
        except:
            pass
        
        input("\nPress Enter to continue...")

# Main Application Loop
def main():
    while True:
        check_low_stock()
        print_header("INVENTORY MANAGEMENT SYSTEM")
        print_menu()
        
        try:
            choice = input(Fore.WHITE + "Enter your choice (1-7): ").strip()
            
            if choice == '1':
                add_inventory()
            elif choice == '2':
                process_sale()
            elif choice == '3':
                update_stock()
            elif choice == '4':
                view_inventory()
                input("\nPress Enter to continue...")
            elif choice == '5':
                view_history()
            elif choice == '6':
                delete_inventory()
            elif choice == '7':
                print_header("THANK YOU FOR USING INVENTORY SYSTEM")
                print(Fore.GREEN + "\nGoodbye! Have a great day!\n")
                break
            else:
                print_error("Invalid choice! Please enter a number between 1-7")
                time.sleep(1)
                
        except Exception as e:
            print_error(f"An error occurred: {e}")
            time.sleep(1)

if __name__ == "__main__":
    main()