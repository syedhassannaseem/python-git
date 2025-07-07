import json
import os

# File to store inventory
INVENTORY_FILE = "iiii.json"

# Load existing inventory or create empty one
def load_inventory():
    if os.path.exists(INVENTORY_FILE):
        with open(INVENTORY_FILE, 'r') as f:
            return json.load(f)
    return {}

# Save inventory to file
def save_inventory(inventory):
    with open(INVENTORY_FILE, 'w') as f:
        json.dump(inventory, f, indent=4)

# Add new item to inventory
def add_item():
    inventory = load_inventory()
    
    item_id = input("Enter item ID: ")
    name = input("Enter item name: ")
    quantity = int(input("Enter quantity: "))
    price = float(input("Enter price: "))
    
    inventory[item_id] = {
        "name": name,
        "quantity": quantity,
        "price": price
    }
    
    save_inventory(inventory)
    print(f"Item {name} added successfully!")

# View all items
def view_items():
    inventory = load_inventory()
    
    if not inventory:
        print("No items in inventory!")
        return
    
    print("\nCurrent Inventory:")
    print("-" * 30)
    for item_id, details in inventory.items():
        print(f"ID: {item_id}")
        print(f"Name: {details['name']}")
        print(f"Quantity: {details['quantity']}")
        print(f"Price: ₹{details['price']:.2f}")
        print("-" * 30)

# Main menu
while True:
    print("\nSimple Stock Inventory System")
    print("1. Add Item")
    print("2. View Items")
    print("3. Exit")
    
    choice = input("Enter your choice (1-3): ")
    
    if choice == '1':
        add_item()
    elif choice == '2':
        view_items()
    elif choice == '3':
        print("Exiting program. Inventory saved.")
        break
    else:
        print("Invalid choice! Please try again.")