import json 
import os
import win10toast
import time
from datetime import datetime
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
       

    else:
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


def Update():
    data = load_inventory()
    for ID,details in data.items():
        id = input("Enter Product ID: ")
        if ID == id:    
            print(f"Current Quantity is {details["Quantity"]}")
        else:
            print("⚠️ Product Not Found!!!")
            break
        try:    
            scanf = int(input("Enter quantity to add/subtract (use - for subtraction): "))
        except ValueError as v:
            print(f"\nEnter Integer Value {v}\n")
            break 
        details["Quantity"] += scanf
        print(f"Update Quantity is {details["Quantity"]}")
        with open(INVENTORYFILE,"w") as z:
            json.dump(data , z ,indent=4)
        break


def delete(): # To delete all json file content 

    with open(INVENTORYFILE, 'w') as file:
      json.dump({},file)
    print(f"\n\nDone..... Now the json file is empty\n\n")

 # History Sale Managment Code


HISTORY = "Sales_History.json"

def dump_Sale(sale): # Save inventory content in json file
        with open(HISTORY,"w") as g :
            json.dump(sale , g ,indent=4)

def load_Sale():# Load inventory data 
    if os.path.exists(HISTORY):
     with open(HISTORY,"r") as h:
          return json.load(h)
    else:
         print("\n⚠️ Inventory Not Found!!\n")
    return {}


def Process_Sale(): # To deduct Product Quantity in invenotry and Generate Sale History
        data = load_inventory()
        history = load_Sale()
        print("\n","-"*5,"Process Sale","-"*5,"\n")
        num =input("Enter product ID ('Exit' for Quit): ")
        for ID , details in data.items():
            if num.upper() == "EXIT":
                print("Exiting...")
                break
            if num == ID:
                print(f"Product name is {details["Name"]}")
                print(f"Available Quantity is: {details["Quantity"]}")
                city = input("Enter City Name: ")
                try:    
                    subt = int(input("Enter Quantity to sell: "))
                except ValueError as v:
                    print(f"⚠️ Enter Integer value only!!⭕⭕ {v}")
                    break
                if subt >= 0:
                    details["Quantity"] -= subt
                    total = subt * details["Price"]
                    print("\n","-"*5,"Recipt","-"*5,"\n")
                    print(f"City {city}")
                    print(f"Product name is {details["Name"]}")
                    print(f"Quantity {subt}")
                    print(f"Unit Price is Rs{details["Price"]}")
                    print(f"Total Bill is Rs{total}")
                    with open(INVENTORYFILE,"w") as x:
                        json.dump(data , x , indent=4)
                    #Sales History Save Code
                    history[True]= {
                        "City": city,
                        "Name" : details["Name"],
                        "Quantity": subt,
                        "Unit_Price":details["Price"],
                        "Total_Price": subt * details["Price"],
                        "Date" : time.strftime("%d""-%B-""%Y"),
                        "Time": str(datetime.now().time())
                    }
                    dump_Sale(history)
                else:
                    print("⚠️ Enter Positive Number🔢")
                break
        else:
            print("⚠️ Please Enter Correct Product ID🙏🏻")
def View_history(): # To see Sales History

    data = load_Sale()

    if not data:
          print("\n⚠️ No Items in Inventory\n")

    print("\nSales History:")
    print("-" * 30)
    for  ID,details in data.items():
        print(f"ID: {ID}")
        print(f"City: {details["City"]}")
        print(f"Name: {details['Name']}")
        print(f"Quantity: {details['Quantity']}")
        print(f"Price: Rs{details['Unit_Price']}")
        print(f"Price: Rs{details['Total_Price']}")
        print(f"Time: {details["Time"]}")
        print(f"Date: {details["Date"]}")
        print("-" * 30)


# Notification pop Code 

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
                        print(f"\n➡️  {details["Name"]} is running low (Only {details["Quantity"]} left!)")
                        print("-"*30)
                        time.sleep(3.4)
        except Exception as e:
            print(f"{e}")
        break
Notification()

while True:
    try:
        print("-"*25,"Inventory Managment System","-"*25)
        print("1- Add Details⭕")
        print("2- Process Sale👀")
        print("3- Update Stock")
        print("4- View Inventory👀")
        print("5- View history")
        print("6- Delete inventory content💥")
        print("7- for Exit🔚")
        choice =  int(input("Enter Number between (1-7): "))
    except ValueError as v:
        print(f"\n⚠️ Enter Integer Number!! {v}")   
        continue 
    if choice == 1:
        add_inventory()
    elif choice == 2:
        Process_Sale()
    elif choice ==3:
        Update()
    elif choice == 4:
        view_inventory()
    elif choice == 5:
        View_history()
    elif choice == 6:
        delete()
    elif choice == 7:
        print("\nThank you for using the Inventory System!🫀")
        break
    else:
        print("⚠️ Please Enter Number between 1-7")
