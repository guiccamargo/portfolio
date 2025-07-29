from tkinter import *
from tkinter import filedialog

from pypdf import PdfReader

from pdf_to_audiobook.speaker import Speaker


def upload_file():
    file_path = filedialog.askopenfilename(initialdir="/",  # Open the dialog box on the root folder
                                           title="Select a File",  # Title of the dialog box
                                           defaultextension=".pdf")
    # Extract Text from PDF
    all_text = ""
    # Path of the PDF file
    try:
        reader = PdfReader(file_path)

        num_pages = len(reader.pages)

        # Extract text from all pages
        for page_num in range(num_pages):
            page = reader.pages[page_num]
            text = page.extract_text(space_width=1)
            all_text += text

        # Remove line breaks
        all_text = all_text.replace("\n", "")

        # Initialize speaker module
        speaker = Speaker()
        # Synthesize audio
        audiobook = speaker.synthesize_speech(text=all_text, voice_id="Emma", engine="standard", output_format="mp3",
                                              text_type="text")
        download_button = Button(root, text="Download Audiobook",
                                 command=lambda: download_audio(speaker=speaker, audio=audiobook))
        download_button.grid(row=3, column=1)
        text_label.config(text="Download your audiobook:")
    except FileNotFoundError:
        text_label.config(text=f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        text_label.config(text=f"An error occurred: {e}")
    finally:
        text_label.grid(row=2, column=1)


def download_audio(speaker, audio):
    # Save audiobook
    files = [('All Files', '*.*')]
    path_to_save = filedialog.asksaveasfile(filetypes=files, defaultextension=".mp3")
    speaker.save_audio_file(audio, path_to_save.name)
    root.quit()


# Create main window
root = Tk()
root.geometry("500x400")
root.title("PDF to Audiobook")

text_label = Label(root, text="")
upload_button = Button(root, text="Select a PDF file", command=upload_file)
upload_button.grid(row=1, column=1)

# Creating Empty Frames to adjust layout
Frame(width=500, height=50).grid(row=0, column=0, columnspan=3)
Frame(width=30, height=400).grid(row=1, rowspan=3, column=0)
Frame(width=30, height=400).grid(row=1, rowspan=3, column=2)

root.mainloop()
