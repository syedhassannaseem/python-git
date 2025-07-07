import json 
import os

INVENTORYFILE = "inventory.json"

def dump_inventory(inventory):
        with open(INVENTORYFILE,"w") as g :
            json.dump(inventory , g ,indent=4)

def load_inventory():
    if os.path.exists(INVENTORYFILE):
     with open(INVENTORYFILE,"r") as h:
          return json.load(h)
    else:
         print("\n⚠️ Inventory Not Found!!\n")
    return {}

def add_inventory():
    inventory = load_inventory()
    ID = input("Enter Product ID: ")

    if ID in inventory:
       print(f"⚠️ Product ID '{ID}' already exists!")

    
    Name = input("Enter Product Name: ")
    try:
        Quantity = int(input("Enter Product Quantity: "))
    except ValueError as v :
         print(f"⚠️ Quantity is always Integer {v}")
    try:
        Price = float(input("Enter Product Price: "))
    except ValueError as v:
         print(f"⚠️ Price is always Integer/float Number {v}")
    Batch_No = input("Enter Product Batch No: ")

    inventory[ID] = {
        "Name" : Name,
        "Quantity" : Quantity,
        "Price" : Price,
        "Batch_No" : Batch_No
    }
    dump_inventory(inventory)
    print("\n✅ Successfully Save Product Details!!\n")


def view_inventory():

    data = load_inventory()

    if not data:
          print("\n⚠️ No Items in Inventory\n")

    print("\nCurrent Inventory:")
    print("-" * 30)
    for item_id, details in data.items():
        print(f"ID: {item_id}")
        print(f"Name: {details['Name']}")
        print(f"Quantity: {details['Quantity']}")
        print(f"Price: ₹{details['Batch_No']}")
        print("-" * 30)


while True:     
    try:
        print("1- for Add Details⭕")
        print("2- for View details👀")
        print("3- for Exit🔚")
        choice =  int(input("Enter Number between (1-3):"))
    except ValueError as v:
        print(f"\n⚠️ Enter Integer Number!! {v}")    
    if choice == 1:
        add_inventory()
    elif choice == 2:
        view_inventory()
    elif choice == 3:
        print("\nThank you for using the Inventory System!")
        break
    else:
        print("⚠️ Please Enter Number between 1-2")


