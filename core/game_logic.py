from enum import Enum


class SquareState(Enum):
    EMPTY = 0
    X = 1
    O = 2


class InvalidMoveException(Exception):
    pass

class Board:
    def __init__(self):
        self.board = [SquareState.EMPTY]*9
        self.current_player = SquareState.O

    def is_empty(self):
        return all([square == SquareState.EMPTY for square in self.board])

    def make_move(self, position):
        if position < 0 or position > 8:
            raise InvalidMoveException("Position is outside of board")

        if self.board[position] != SquareState.EMPTY:
            raise InvalidMoveException("Square is already taken")

        self.board[position] = self.current_player
        self.current_player = SquareState.X if self.current_player == SquareState.O else SquareState.O