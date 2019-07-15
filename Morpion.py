from Socket import Socket


class Player:
    """self, number (int), pawn (str), name (str)
    A player of the party"""
    def __init__(self, number: int, pawn: str, name: str, connexion=None):
        """self, number (int), pawn (str), name (str)
        A player of the party"""
        self.number = number  # The number of the player
        self.pawn = pawn  # The pawn of the player
        self.name = name  # The name of the player
        self.pawns = list()  # All the pawns on the grid of the player
        self.points = 0  # The points of the player
        self.connexion = connexion

    def add_pawn(self, enemy: list, pos: int):
        """self, enemy (list), pos (int)
        Check if position is free by the enemy grid and add to the grid"""
        if (pos not in self.pawns) and (pos not in enemy):  # Check the enemy grid
            self.pawns.append(pos)  # Add the pawn to the player grid
            return True
        else:
            return False

    def check(self):
        """self
        Check if the player have a matching grid for win"""
        for l in [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]:  # wins list
            if len(set(self.pawns + l)) <= len(self.pawns + l) - 3:  # Check if the set lose 3 pawns
                return True
        return False

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
        Return the number of player's panws"""
        return len(self.pawns)

    def __iter__(self):
        """self
        Setup iterable for pawns list"""
        self.iterable = 0
        return self

    def __next__(self):
        """self
        Return iterable of pawns"""
        if self.iterable <= len(self.pawns)-1:  # check is not exceed
            self.iterable += 1
            return self.pawns[self.iterable-1]
        else:
            raise StopIteration


class Board:
    """self, p1_pawn (str), p1_name (str), p2_pawn (str), p2_name (str)
    A party object"""
    def __init__(self, p1_pawn: str = "O", p1_name: str = "Player1", p2_pawn: str = "X", p2_name: str = "Player2"):
        """self, p1_pawn (str), p1_name (str), p2_pawn (str), p2_name (str)
        A party object"""
        # Security if conflict with players pawns and name
        if p1_pawn == p2_pawn:
            raise ValueError("The pawns are the same !")
        elif p1_name == p2_name:
            raise ValueError("The name are the same !")

        self.players = [Player(1, p1_pawn, p1_name), Player(2, p2_pawn, p2_name)]  # Set players
        self.curr_turn = self.players  # Set turn order

    def check(self):
        """self
        Check if someone win the game"""
        if (len(self.players[0]) + len(self.players[1]) == 9)\
                and not(self.players[0].check() or self.players[1].check()):  # Check equality
            return 3
        elif self.players[0].check():  # Check player 1
            return 1
        elif self.players[1].check():  # Check player 2
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
        board = f"""P1: {self.players[0].points} | P2: {self.players[1].points}
[{pawns[0]},{pawns[1]},{pawns[2]}]
[{pawns[3]},{pawns[4]},{pawns[5]}]
[{pawns[6]},{pawns[7]},{pawns[8]}]
{self.players[0]}: {self.players[0].points}/{self.players[1]}: {self.players[1].points}"""
        print(board)


class Server(Socket):
    def __init__(self, host: str = "localhost", port: int = 3621):
        super().__init__()
        self.socket.bind((host, port))
        self.socket.listen(2)
        self.board = Board()

        for p in self.board.players:
            self.connexion(p)

    def connexion(self, p):
        while True:
            print("Await for a player connexion")
            p.connexion = self.connect_client(self.socket, 1)
            print("Got a connexion, wait or check")

            self.send(p.connexion, "pawn")
            p.paws = self.receive(p.connexion)
            self.send(p.connexion, "name")
            p.name = self.receive(p.connexion)
            print(f"Player {p.name} online")
            return True


class Client(Socket):
    def __init__(self, host: str, port: int, pawn: str, name: str):
        super().__init__()
        self.connect_server(self.socket, host, port, 1)

        if self.receive(self.socket) == "pawn":
            self.send(self.socket, pawn)
        else:
            raise ConnectionError("Bad pawn demand")
        if self.receive(self.socket) == "name":
            self.send(self.socket, name)
        else:
            raise ConnectionError("Bad name demand")
