


class Board:
    def __init__(self):
        self.board = [""]*9
        self.current_player = "O"

    def is_empty(self):
        return all([square == "" for square in self.board])

    def make_move(self, position):
        self.board[position] = self.current_player
        self.current_player = "X" if self.current_player == "O" else "O"