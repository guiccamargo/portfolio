from datetime import datetime
from tkinter import *

# Start time counter
start = datetime.now()
current_time = datetime.now()
# Create window
root = Tk()
root.geometry("800x600")
root.title("Disappearing Text")
# Create text box
text_box = Text(root, font=12)
text_box.grid(row=1, column=0, columnspan=3, padx=20)
# Create Timer
timer_label = Label(root, text="0", font=("arial", 18, "bold"), pady=20)
timer_label.grid(row=0, column=2)


def update_screen():
    """
    Update the timer and text box
    """
    global current_time
    global start
    # Calculate interval
    interval = current_time - start
    interval = interval.seconds
    # Check if the interval before the last action is smaller than 10 seconds.
    if interval < 10:
        # Chance font color to show user that the time is running out.
        if interval > 5:
            text_box.config(fg="red")
            timer_label.config(fg="red")
            current_time = datetime.now()
        else:
            # Changing font color to default
            text_box.config(fg="black")
            timer_label.config(fg="black")
    else:
        # Delete text when time is out
        text_box.delete("0.0", END)
        start = datetime.now()
    # Rerun this function
    root.after(1000, update_screen)
    # Update timer label
    timer = StringVar()
    timer.set(interval)
    timer_label.config(textvariable=timer)
    # Update current time
    current_time = datetime.now()


def press_key(*args):
    """
    Update the starting time when any key is pressed
    """
    global start
    global current_time
    start = current_time = datetime.now()


# Run main loop
text_box.bind("<Key>", press_key)
root.after(1000, update_screen)
root.mainloop()
