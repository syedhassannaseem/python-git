# Simple Alarm Clock

# Play a sound or print a message after a set time.

import win10toast
from datetime import datetime

try:
    tim = input("Enter time like this (HH:MM) ")
    datetime.strptime(tim, "%H:%M")
    while True:
        alarm = datetime.now().strftime("%H:%M")
        if(alarm == tim):
            win10toast.ToastNotifier().show_toast(
                "Alaram Clock"

                "\nWake up, Time is up",

                  duration=2,

                  threaded=True
            )
except ValueError:
    print("Error: Please enter time in HH:MM format (e.g., 14:30)")