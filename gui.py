from tkinter import Tk, Label, Button, Entry, Frame, LabelFrame, StringVar
from tkinter.messagebox import showwarning, showerror, askokcancel
from Morpion import Board

DEFAULT_BUTTON = "    "  # Default Morpion button text


def on_closing():
    """When a windows want to close, show a warning and exit correctly the program"""
    if askokcancel("Quit", "Do you want to quit?"):  # Ask to close
        exit(0)


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
    turn.set(f"{board.curr_turn[0]} turn !")  # Update player turn display


def set_players():
    """Set players pawns and name before start the party"""
    if "" in [p1_pawn.get(), p1_name.get(), p2_pawn.get(), p2_name.get()]:  # check if any empty entry
        showerror("Error", "A entry is blank !")  # Show a warning
    elif p1_pawn.get() == p2_pawn.get():  # Check if players pawns are same
        showerror("Error", "Players pawns are identical !")  # Show a warning
    elif p1_name.get() == p2_name.get():  # Check if players names are same
        showerror("Error", "Players names are identical !")  # Show a warning
    else:  # If everything is fine
        players.destroy()  # Quite the windows to let the party begin


# Create players config window
players = Tk()
players.title("Players configs")
players.protocol("WM_DELETE_WINDOW", on_closing)  # Set action when windows is closing

# Create a frame for players info and submit button
players_f = Frame(players)
players_f.pack()

# Create two frame for each player info
players_p1f = LabelFrame(players_f, text="Player 1")
players_p2f = LabelFrame(players_f, text="Player 2")
players_p1f.grid(row=0, column=0)
players_p2f.grid(row=0, column=1)

p1_pawn, p1_name, p2_pawn, p2_name = StringVar(), StringVar(), StringVar(), StringVar()  # Setup entry value

# Generate symmetrically widgets for player infos
for i in [[players_p1f, p1_pawn, p1_name], [players_p2f, p2_pawn, p2_name]]:  # List contain the frame and the entry var
    Label(i[0], text="Player name:").pack()
    Entry(i[0], textvariable=i[2], width=20).pack()
    Label(i[0], text="Player pawn:").pack()
    Entry(i[0], textvariable=i[1], width=5).pack()

Button(players, text="Submit", command=set_players).pack()  # Create the submit button

players.mainloop()

board = Board(p1_pawn.get(), p1_name.get(), p2_pawn.get(), p2_name.get())  # Create a party board

# Create party window
windows = Tk()
windows.title("Morpion")
windows.protocol("WM_DELETE_WINDOW", on_closing)  # Set action when windows is closing

Label(windows, text="Morpion").pack()  # Add a text

# Create a frame for the grid
f = Frame(windows)
f.pack()

# Setup variable string display
turn = StringVar()
scoreboard = StringVar()
turn.set(f"{board.curr_turn[0]} turn !")
scoreboard.set(f"{board.player1}: {board.player1.points}/{board.player2}: {board.player2.points}")

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
