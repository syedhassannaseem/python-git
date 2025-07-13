import json 
import os
import win10toast
import time

INVENTORYFILE = "inventory.json"

def dump_inventory(inventory): # Save inventory content in json file
        with open(INVENTORYFILE,"w") as g :
            json.dump(inventory , g ,indent=4)

def load_inventory():# Load inventory data 
    if os.path.exists(INVENTORYFILE):
     with open(INVENTORYFILE,"r") as h:
          return json.load(h)
    else:
         print("\n⚠️ Inventory Not Found!!\n")
    return {}

def add_inventory():# Add invenotry Products  
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


def view_inventory(): # To see all Store Products in inventory 

    data = load_inventory()

    if not data:
          print("\n⚠️ No Items in Inventory\n")

    print("\nCurrent Inventory:")
    print("-" * 30)
    for item_id, details in data.items():
        print(f"ID: {item_id}")
        print(f"Name: {details['Name']}")
        print(f"Quantity: {details['Quantity']}")
        print(f"Price: Rs{details['Price']}")
        Total = details["Quantity"] * details["Price"]
        print(f"Total Price is Rs{Total}")
        print(f"Batch no: {details['Batch_No']}")
        print("-" * 30)
    

def Process_Sale(): # To deduct Product Quantity in invenotry
        data = load_inventory()
        print("\n","-"*5,"Process Sale","-"*5,"\n")
        num =input("Enter product ID ('Exit' for Quit): ")
        for ID , details in data.items():
            if num.upper() == "EXIT":
                print("Exiting...")
                break
            if num == ID:
                print(f"Product name is {details["Name"]}")
                print(f"Available Quantity is: {details["Quantity"]}")
                try:    
                    subt = int(input("Enter Quantity to sell: "))
                except ValueError as v:
                    print(f"⚠️ Enter Integer value only!!⭕⭕ {v}")
                if subt >= 0:
                    details["Quantity"] -= subt
                    total = subt * details["Price"]
                    print("\n","-"*5,"Recipt","-"*5,"\n")
                    print(f"Product name is {details["Name"]}")
                    print(f"Quantity {subt}")
                    print(f"Unit Price is Rs{details["Price"]}")
                    print(f"Total Bill is Rs{total}")
                    with open(INVENTORYFILE,"w") as x:
                        json.dump(data , x , indent=4)
                else:
                    print("⚠️ Enter Positive Number🔢")
                break
        else:
            print("⚠️ Please Enter Correct Product ID🙏🏻")

def Update():
    data = load_inventory()
    for ID,details in data.items():
        id = input("Enter Product ID: ")
        if ID == id:    
            print(f"Current Quantity is {details["Quantity"]}")
        else:
            print("⚠️ Product Not Found!!!")
            break     
        scanf = int(input("Enter quantity to add/subtract (use - for subtraction): "))
        details["Quantity"] += scanf
        print(f"Update Quantity is {details["Quantity"]}")
        with open(INVENTORYFILE,"w") as z:
            json.dump(data , z ,indent=4)
        break

def delete(): # To delete all json file content 

    with open(INVENTORYFILE, 'w') as file:
      json.dump({},file)
    print(f"\n\nDone..... Now the json file is empty\n\n")
        
def Notification():  # To Show Notification When Product reached to End
    while True:
        data = load_inventory()
        to = win10toast.ToastNotifier()
        try:
            for ID , details in data.items():
                if details["Quantity"] <= 500:
                        to.show_toast(
                            "⚠️ WARNING",
                            f"➡️ The Products is running out soon",
                            duration=3,
                            threaded=True
                        )
                        print(f"➡️  {details["Name"]} is running low (Only {details["Quantity"]} left!)")
                        print("-"*30)
                        time.sleep(3.4)
        except Exception as e:
            print(f"{e}")
        break
Notification()

while True:
    try:
        print("-"*50)
        print("1- Add Details⭕")
        print("2- View details👀")
        print("3- Process Sale👀")
        print("4- Update Stock")
        print("5- for Exit🔚")
        print("6- Delete inventory content💥")
        choice =  int(input("Enter Number between (1-6): "))
    except ValueError as v:
        print(f"\n⚠️ Enter Integer Number!! {v}")    
    if choice == 1:
        add_inventory()
    elif choice == 2:
        view_inventory()
    elif choice ==3:
        Process_Sale()
    elif choice == 4:
        Update()
    elif choice == 5:
        print("\nThank you for using the Inventory System!🫀")
        break
    elif choice == 6:
        delete()
    else:
        print("⚠️ Please Enter Number between 1-6")
