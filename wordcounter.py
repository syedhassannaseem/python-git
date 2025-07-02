filename= input("Enter your file name with their extension (name.txt): ")
lst = []

with open(f"{filename}","r") as r:# This is used to read file

    m = r.read() 

lst.append(m) #This is used to append text of "m" in "lst"

for i in lst:
    count = len(i)

print(f"The file contain {count} words")
