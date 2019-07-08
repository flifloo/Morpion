from tkinter import Tk, Label, Button, Frame, StringVar
from tkinter.messagebox import showwarning
from Morpion import Board

DEFAULT_BUTTON = "    "  # Default Morpion button text


def result(r: int):
    """r (int): 0 = Anyone win, 1 = Player 1 win, 2 = Player 2 win, 3 = Equality
    Use the result of a party to reset and announce if necessary"""
    if r:  # If 0, nothing to do
        if r in [1, 2]:  # If someone yin, get the last person who play and mark as winner
            r1, r2, text = 2, 0, f"{board.curr_turn[1]} win !"
        elif r == 3:  # Set equality
            r1, r2, text = 1, 1, "Equality"
        board.curr_turn[1].gameover(r1)
        board.curr_turn[0].gameover(r2)
        showwarning("Turn end", text)  # Announce the result
        for b in range(9):  # Reset all the buttons
            buttons[b].config(state="normal", text=DEFAULT_BUTTON)
        scoreboard.set(f"{board.player1}: {board.player1.points}/{board.player2}: {board.player2.points}")  # Scoreboard


def case(posi: int):
    """posi (int) : Position of the button on the grid
    Action when a button is used"""
    buttons[posi].config(state="disabled", text=board.curr_turn[0].pawn)  # Disable and set player pawn on the button
    result(board.turn(posi))  # Make player turn and return the result of the party
    turn.set(board.curr_turn[0])  # Update player turn display


board = Board()  # Create a board

# Create base window
windows = Tk()
windows.title("Morpion")

Label(windows, text="Morpion").pack()  # Add a text

# Create a frame for the grid
f = Frame(windows)
f.pack()

# Setup variable string display
turn = StringVar()
scoreboard = StringVar()

turn.set(board.curr_turn[0])
scoreboard.set("0/0")

Label(windows, textvariable=turn).pack()
Label(windows, textvariable=scoreboard).pack()

# Create button on the grid
n = 0
buttons = list()
for line in range(3):
    for column in range(3):
        buttons.append(Button(f, text=DEFAULT_BUTTON, command=lambda n=n: case(n)))  # Create and add to the list
        buttons[n].grid(row=line, column=column)  # Set the button to the grid
        n += 1

windows.mainloop()
