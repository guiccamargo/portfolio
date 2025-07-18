from tkinter import *
from tkinter import ttk, filedialog

from PIL import ImageTk, Image, ImageGrab

# Create main window
root = Tk()
root.geometry("500x400")
root.title("Watermarking App")


def download_img(frame, new_image):
    """
    Saves the watermarked image to a file.
    :param frame: Window to display the image
    :param new_image: Canvas to be saved as an image
    """
    files = [('PNG Image', '*.png'), ('JPEG Image', '*.jpg'), ('All Files', '*.*')]
    # Ask user to select the path to save the image
    path_to_save = filedialog.asksaveasfile(filetypes=files, defaultextension=".png")

    # Find the position of the image on screen
    x = 2 + frame.winfo_rootx() + new_image.winfo_x()
    y = 2 + frame.winfo_rooty() + new_image.winfo_y()
    x1 = x + new_image.winfo_width() - 6
    y1 = y + new_image.winfo_height() - 6

    # Crop the image and save file
    ImageGrab.grab().crop((x, y, x1, y1)).save(path_to_save)

    # Close image window
    frame.destroy()
    root.destroy()


def upload_img():
    """
    Upload an image to the App
    """

    # Ask user to select an image
    file_path = filedialog.askopenfilename(initialdir="/",  # Open the dialog box on the root folder
                                           title="Select a File",  # Title of the dialog box
                                           )

    # Create a window to display an image
    img_window = Toplevel(root)
    img_window.title(file_path.split("/")[-1])
    # Withdraw root window
    root.withdraw()
    # Open the image file
    img = Image.open(file_path)
    # Resize image to a standard size
    img = img.resize((600, 800))
    # Turn the image into a Tk widget
    tk_img = ImageTk.PhotoImage(img)
    # Create a canvas widget to insert watermark
    canvas = Canvas(img_window, height=tk_img.height(), width=tk_img.width())
    # Place canvas widget
    canvas.pack(fill="both", expand=True)
    # Create the image on canvas
    canvas.create_image(0, 0, image=tk_img, anchor="nw")
    # Open watermark image as a png file
    watermark = Image.open("./img/watermark.png")
    # Create watermark widget
    tk_watermark = ImageTk.PhotoImage(watermark)
    # Place watermark on image
    canvas.create_image(tk_img.width() * 0.7, tk_img.height() * 0.7, image=tk_watermark)
    # Show button to save the image
    download_button = Button(img_window, text="Download Image", command=lambda: download_img(img_window, canvas))
    # Place the button
    download_button.pack()
    # Run image window loop
    img_window.mainloop()


# Show title
title_label = ttk.Label(root, text="Welcome to the Watermarking Marker", font=("Arial", 18), padding=(0, 140, 0, 20))
title_label.pack()
# Show upload button
upload_button = Button(text="Upload image", command=upload_img)
upload_button.pack()
# Run root main loop
root.mainloop()
