from datetime import datetime
from random import choice
from tkinter import *

from typing_speed_app import texts

# Index of the word to be typed
CURRENT_WORD = 0
# Count corrected typed words
WORD_COUNT = 0
# Index of the last word typed
LAST_INDEX = "1.0"

# Start Tk window
root = Tk()
root.geometry("800x600")

# Selecting sample text
sample = choice(texts.samples).strip()
# Split words in the sample
words_in_samples = sample.split(" ")
# Total amount words
NUM_WORDS = len(words_in_samples)
# Show sample text
sample_text = Text(root, wrap="word", font=18, relief="ridge", height=5)

# Empty frames to set the layout
Frame(root, width=50).grid(row=0, column=0, rowspan=3)
Frame(root, width=50).grid(row=0, column=2, rowspan=3)
Frame(root, height=50).grid(row=2, column=1)

# Layout of the sample text box
sample_text['borderwidth'] = 2
sample_text['relief'] = 'sunken'

# Start timer
current_time = datetime.now()
timer = Label(text="Start typing", font=18)
timer.grid(row=0, column=1)

# Insert sample text
sample_text.insert(END, sample)
sample_text.grid(row=1, column=1)
sample_text.config(state="disabled")


def check_word(index: int, right: bool = True):
    """
    Checks if the word that has been typed matches the highlighted word.
    :param index: The index of the word in the sample
    :param right:  Informs if the user typed the right word
    """
    # Load global variables
    global WORD_COUNT
    global LAST_INDEX
    # Find the current word to be checked
    search_word = words_in_samples[index]
    # Set the index of the last correct word
    start_index = LAST_INDEX
    # Search the word on the users input
    start_index = sample_text.search(search_word, start_index, END)
    end_index = f"{start_index}+{len(search_word)}c"

    if right:
        # Config highlight tag for the current word to be typed
        sample_text.tag_config("highlight", background="yellow", foreground="black")
        # Increase counter of right words
        WORD_COUNT += 1
        # Increase index of the last word
        LAST_INDEX = start_index.split(".")[0] + "." + str(int(start_index.split(".")[-1]) + 1)
        # Calculate time interval
        set_time = datetime.now() - current_time
        if set_time.seconds > 0:
            # Show current typing speed
            timer.config(text=f"{round(WORD_COUNT * 60 / set_time.seconds, 1)} words/min")
    else:
        # Config highlight tag for a wrong typed word
        sample_text.tag_config("highlight", background="red", foreground="black")
        start_index = LAST_INDEX
    # Update index of the last word
    LAST_INDEX = start_index.split(".")[0] + "." + str(int(start_index.split(".")[-1]) - 1)
    # Highlight word
    sample_text.tag_add("highlight", start_index, end_index)


# Show text box for the user to type
user_text = Text(root, font=18)
# Check for users input
check_word(CURRENT_WORD)
# Place text box
user_text.grid(row=3, column=1)


def send(*args):
    """
    Trigger the check_word function when the user presses space.
    """
    # Get global variable
    global CURRENT_WORD
    # Finish App
    if WORD_COUNT == NUM_WORDS:
        # Destroy previous widget
        sample_text.destroy()
        user_text.destroy()
        timer.grid_forget()
        # Show result window
        Label(text="Your typing speed is:", font=18).grid(row=0, column=1)
        timer.grid(row=1, column=1)
    else:
        # Update highlighted word
        sample_text.tag_delete("highlight")
        user_input = user_text.get("1.0", "end-1c")
        # Check if user typed right
        if user_input.split(" ")[-1] == words_in_samples[CURRENT_WORD]:
            # Increase word index
            CURRENT_WORD += 1
            check_word(CURRENT_WORD)
        else:
            check_word(CURRENT_WORD, right=False)


user_text.bind("<space>", send)

root.mainloop()
