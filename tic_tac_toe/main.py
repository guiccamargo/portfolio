from tkinter import *
from tkinter import ttk

from PIL import Image, ImageTk

PLAYER_1 = []
PLAYER_2 = []
NEXT_TO_PLAY = 1
COUNTER = 9
root = Tk()
root.geometry("600x600")
root.title("Tic Tac Toe")

BOARD = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]


def check_winner(board):
    # Check rows
    for row in board:
        if row[0] == row[1] == row[2] and row[0] != ' ':
            return row[0]  # Return the winning player's mark
    # Check columns
    for col_index in range(3):
        if board[0][col_index] == board[1][col_index] == board[2][col_index] and board[0][col_index] != ' ':
            return board[0][col_index]

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != ' ':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != ' ':
        return board[0][2]

    # No winner yet
    return None


mainframe = ttk.Frame(root, height=600, width=600)

x_image = Image.open("img/x.png")
resized_x_image = x_image.resize((196, 196))
tk_x_image = ImageTk.PhotoImage(resized_x_image)

o_image = Image.open("img/O.png")
resized_o_image = o_image.resize((196, 196))
tk_o_image = ImageTk.PhotoImage(resized_o_image)


def generate_x_image(img):
    return Label(mainframe, image=img, relief='raised')


def on_click(event):
    global NEXT_TO_PLAY
    global COUNTER
    global BOARD
    current_frame = event.widget
    if current_frame.widgetName != "label":
        if event.num == 1 and NEXT_TO_PLAY == 1:
            pos = current_frame.grid_info()
            row, column = pos["row"], pos["column"]
            current_frame.destroy()
            PLAYER_1.append((row, column))
            NEXT_TO_PLAY = 3
            current_img = generate_x_image(tk_x_image)
            current_img.grid(row=row, column=column)
            BOARD[row][column] = "Player 1"
            COUNTER -= 1
        elif event.num == 3 and NEXT_TO_PLAY == 3:
            pos = current_frame.grid_info()
            row, column = pos["row"], pos["column"]
            current_frame.destroy()
            PLAYER_2.append((row, column))
            current_img = generate_x_image(tk_o_image)
            current_img.grid(row=row, column=column)
            NEXT_TO_PLAY = 1
            COUNTER -= 1
            BOARD[row][column] = "Player 2"
        else:
            pass

    if len(PLAYER_2) > 2 or len(PLAYER_1) > 2:
        winner = check_winner(BOARD)

        if winner:
            mainframe.destroy()
            game_over = Label(root, text=f"{winner} Won!", font=("Arial", 45))
            game_over.place(x=120, y=250)
        elif COUNTER < 1:
            mainframe.destroy()
            game_over = Label(root, text="It's a Draw!", font=("Arial", 45))
            game_over.place(x=120, y=250)


def generate_table():
    frame = ttk.Frame(mainframe, width=200, height=200, style='Danger.TFrame')
    frame['borderwidth'] = 2
    frame['relief'] = 'raised'
    frame.grid(row=0, column=0)

    frame2 = ttk.Frame(mainframe, width=200, height=200, style='Danger.TFrame')
    frame2['borderwidth'] = 2
    frame2['relief'] = 'raised'
    frame2.grid(row=0, column=1)

    frame3 = ttk.Frame(mainframe, width=200, height=200, style='Danger.TFrame')
    frame3['borderwidth'] = 2
    frame3['relief'] = 'raised'
    frame3.grid(row=0, column=2)

    frame4 = ttk.Frame(mainframe, width=200, height=200, style='Danger.TFrame')
    frame4['borderwidth'] = 2
    frame4['relief'] = 'raised'
    frame4.grid(row=1, column=0)

    frame5 = ttk.Frame(mainframe, width=200, height=200, style='Danger.TFrame')
    frame5['borderwidth'] = 2
    frame5['relief'] = 'raised'
    frame5.grid(row=1, column=1)

    frame6 = ttk.Frame(mainframe, width=200, height=200, style='Danger.TFrame')
    frame6['borderwidth'] = 2
    frame6['relief'] = 'raised'
    frame6.grid(row=1, column=2)

    frame7 = ttk.Frame(mainframe, width=200, height=200, style='Danger.TFrame')
    frame7['borderwidth'] = 2
    frame7['relief'] = 'raised'
    frame7.grid(row=2, column=0)

    frame8 = ttk.Frame(mainframe, width=200, height=200, style='Danger.TFrame')
    frame8['borderwidth'] = 2
    frame8['relief'] = 'raised'
    frame8.grid(row=2, column=1)

    frame9 = ttk.Frame(mainframe, width=200, height=200, style='Danger.TFrame')
    frame9['borderwidth'] = 2
    frame9['relief'] = 'raised'
    frame9.grid(row=2, column=2)


mainframe.grid()
generate_table()

root.bind("<Button>", on_click)
root.mainloop()
