# Basic Countdown Timer
# Take user input for seconds and count down to zero
import time
try:
    a = int(input("Enter seconds: "))
    for i in range(0,a):
        print(i)
        time.sleep(1)
except ValueError:
        print("Enter correct value")