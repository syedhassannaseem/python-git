import random
import string
def gen():
    try:
        length = int(input("enter the digit how long ur password is: "))
        uap =string.ascii_uppercase
        lap =string.ascii_lowercase
        sym =string.punctuation
        bap =string.ascii_letters

        al = uap +lap +sym + bap

        password = ''.join(random.choice(al) for _ in range(length))
        print(password)
    except ValueError:
        print("please Enter integer value")

gen()



