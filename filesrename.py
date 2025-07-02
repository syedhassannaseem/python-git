import os
user = int(input("'0' for make files and '1' for rename files: "))
if user not in (0,1):
    print("Error Please Enter number '0' or '1'")
if(user == 0):
    for i in range(1,100):
        destination = input("Enter your folder: ")
        name = input("Enter You file name")
        with open(f"{destination}/{name}{i}.txt" , "w") as f:
            f.write(f"Hello world{i}")
        print("100 Files successfully Created")
elif(user == 1):
    des = input("Enter your folder: ")
    old_name = input("Enter the name of old file with their extention (name.txt): ")
    new_name = input("Enter the name of new file with their extention (name.txt): ")
    for j in range(1,100):
        try:
            os.rename(f"{des}/{old_name}{j}.txt" , f"{des}/{new_name}{j}.txt")
        except Exception as e:
            print(f"Please Enter Correct destination or file name {e}")
        except FileNotFoundError as k:
            print(f"File cannot be file {k}")
    print("File successfully renamed")


