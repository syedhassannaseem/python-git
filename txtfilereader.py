foldername = input("Enter your folder name that contain the file: ")
filename = input("Enter your txt file name: ")
try:
    v = open(f"{foldername}/{filename}.txt","r")
    print(v.read())
except Exception as e:
    print(f"You give wrong input {e}")