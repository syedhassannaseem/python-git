import random
print("Gun for \'1\' , Snake for \'2\' , Water for \'3\'\n\n")
for i in range(1,1100): 
 computer=random.randint(1,3)
 user=int(input("What do u want to choice, \'Gun-1\',\'Snake-2\',\'Water-3\': "))
 print("\n")
 if(user==computer):
    print("Draw\n")
 elif(user==1 and computer==2):
    print(f"You select {user}-Gun\n")
    print(f"Computer select {computer}\n")
    print("You Won")
 elif(user==2 and computer==1):
    print(f"You select {user}-Snake\n")
    print(f"Computer select {computer}\n")
    print("Computer Won")
 elif(user==1 and computer==3):
    print(f"You select {user}-Gun\n")
    print(f"Computer select {computer}\n")
    print("You Won")
 elif( user==3 and computer==1):
    print(f"You select {user}-Water\n")
    print(f"Computer select {computer}\n")
    print("Computer Won")
 elif(user==2 and computer==3):
    print(f"You select {user}-Snake\n")
    print(f"Computer select {computer}\n")
    print("You Won")
 elif(user==3 and computer==2 ):
    print(f"You select {user}-Water\n")
    print(f"Computer select {computer}\n")
    print("Computer Won")
 elif(user==3 and computer==2):
     print(f"You select {user}-Water\n")
     print(f"Computer select {computer}\n")
     print("You Won")
 elif( user==2 and computer==3 ):
     print(f"You select {user}-Snake\n")
     print(f"Computer select {computer}\n")
     print("Computer Won")
 else:
     print("invalid number")
    