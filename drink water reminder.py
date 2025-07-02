import win10toast 
import time
to = win10toast.ToastNotifier()# Create a ToastNotifier object that will handle the notification display
while True:
    time.sleep(3)
    to.show_toast(   # Title of the notification (appears in bold at the top)
        

        "Drink water Reminder", # header of the notification


        "Pani pee lo yar", # message of the notification

        duration= 2, # this is a duration how much time the noticiactio appear

        # icon_path="drink-water.ico",# this is use to add icon the icon extension must be end with .ico extention
        
        threaded=True  # When True, runs the notification in a separate thread
        # Allows your program to continue executing while notification shows
        # If False, program execution pauses until notification disappears
    )