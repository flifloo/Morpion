class Player:
    """self, number (int), pawn (str), name (str)
    A player of the party"""
    def __init__(self, number: int, pawn: str, name: str):
        """self, number (int), pawn (str), name (str)
        A player of the party"""
        self.number = number  # The number of the player
        self.pawn = pawn  # The paw of the player
        self.name = name  # The name of the player
        self.pawns = list()  # All the paws on the grid of the player
        self.points = 0  # The points of the player

    def add_pawn(self, enemy: list, pos: int):
        """self, enemy (list), pos (int)
        Check if position is free by the enemy grid and add to the grid"""
        if (pos not in self.pawns) and (pos not in enemy):  # Check the enemy grid
            self.pawns.append(pos)  # Add the paw to the player grid
            return True
        else:
            return False

    def check(self):
        """self
        Check if the player have a matching grid for win"""
        return (
            # Horizontal check
            (  # First line
                (0 in self.pawns) and (1 in self.pawns) and (2 in self.pawns)
            ) or (  # Second line
                (3 in self.pawns) and (4 in self.pawns) and (5 in self.pawns)
            ) or (  # Third line
                (6 in self.pawns) and (7 in self.pawns) and (8 in self.pawns)
            ) or (  # Vertical check
                # First line
                (0 in self.pawns) and (3 in self.pawns) and (6 in self.pawns)
            ) or (  # Second line
                (1 in self.pawns) and (4 in self.pawns) and (7 in self.pawns)
            ) or (  # Third line
                (2 in self.pawns) and (5 in self.pawns) and (8 in self.pawns)
            ) or (  # Cross check
                # Top-left to bottom-right
                (0 in self.pawns) and (4 in self.pawns) and (8 in self.pawns)
            ) or (  # Bottom-left to top-right
                (2 in self.pawns) and (5 in self.pawns) and (6 in self.pawns)
            ))

    def gameover(self, result: int):
        """self, result (int): 0 = Loose, 1 = Equality, 2 = Win
        Reset player grid and add points from the result of the party"""
        self.pawns = list()  # Grid reset
        self.points += result  # Add result

    def __str__(self):
        """self
        Send back the player's name"""
        return self.name

    def __int__(self):
        """self
        Send back the player's number"""
        return self.number

    def __len__(self):
        """self
        Return the number of player's paws"""
        return len(self.pawns)

    def __iter__(self):
        """self
        Setup iterable for paws list"""
        self.iterable = 0
        return self

    def __next__(self):
        """self
        Return iterable of paws"""
        if self.iterable <= len(self.pawns)-1:  # check is not exceed
            self.iterable += 1
            return self.pawns[self.iterable-1]
        else:
            raise StopIteration


class Board:
    """self, p1_paw (str), p1_name (str), p2_paw (str), p2_name (str)
    A party object"""
    def __init__(self, p1_paw: str, p1_name : str, p2_paw: str, p2_name: str):
        """self, p1_paw (str), p1_name (str), p2_paw (str), p2_name (str)
        A party object"""
        # Security if conflict with players paws and name
        if p1_paw == p2_paw:
            raise ValueError("The pawns are the same !")
        elif p1_name == p2_name:
            raise ValueError("The name are the same !")

        self.player1 = Player(1, p1_paw, p1_name)  # Set player 1
        self.player2 = Player(2, p2_paw, p2_name)  # Set player 2
        self.curr_turn = [self.player1, self.player2]  # Set turn order

    def check(self):
        """self
        Check if someone win the game"""
        if ((len(self.player1) == 4) and (len(self.player2) == 4))\
                and not (self.player1.check() and not self.player2.check()):  # Check equality
            return 3
        elif self.player1.check():  # Check player 1
            return 1
        elif self.player2.check():  # Check player 2
            return 2
        else:  # If nobody win
            return 0

    def turn(self, pos: int):
        """self, pos (int)
        Make a turn from the play order and the given position"""
        if self.curr_turn[0].add_pawn(self.curr_turn[1], pos):  # Add a pawn if possible on the grid
            self.curr_turn = self.curr_turn[::-1]  # Change turn order
            return self.check()  # Return the result of the party
        else:  # If position is not valid, return 4 as an error
            return 4

    def show(self):
        """self
        Show a basic text grid"""
        pawns = dict()
        # Set default grid text
        for i in range(9):
            pawns[i] = "   "
        # For each player entry get their grid
        for p in self.curr_turn:
            for i in list(p):
                pawns[i] = p.pawn
        # Format and print the grid from the dict
        board = f"""P1: {self.player1.points} | P2: {self.player2.points}
[{pawns[0]},{pawns[1]},{pawns[2]}]
[{pawns[3]},{pawns[4]},{pawns[5]}]
[{pawns[6]},{pawns[7]},{pawns[8]}]
{self.player1}: {self.player1.points}/{self.player2}: {self.player2.points}"""
        print(board)