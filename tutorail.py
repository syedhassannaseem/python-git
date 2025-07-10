from winotify import Notification, audio

alert = Notification(
    app_id="Inventory App",
    title="Stock Kam Hua Hai!",
    msg="Product XYZ sirf 5 bacha hai! Jaldi order karein.",
    duration="short",  # 5 secs (ya "short" / "long")
)


# Sound Add Karne ke Liye
alert.set_audio(audio.Reminder, loop=False)

# Notification Show Karein
alert.show()