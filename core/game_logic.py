from enum import Enum

WINNING_COMBOS = [
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
]


class SquareState(Enum):
    EMPTY = 0
    X = 1
    O = 2


class Result(Enum):
    NOT_FINISHED = 0
    DRAW = 1
    X_WINS = 2
    O_WINS = 3


class InvalidMoveException(Exception):
    pass


class Board:
    def __init__(self):
        self.board = [SquareState.EMPTY] * 9
        self.current_player = SquareState.O

    def is_empty(self):
        return all([square == SquareState.EMPTY for square in self.board])

    def make_move(self, position):
        if position < 0 or position > 8:
            raise InvalidMoveException("Position is outside of board")

        if self.board[position] != SquareState.EMPTY:
            raise InvalidMoveException("Square is already taken")

        self.board[position] = self.current_player
        self.current_player = (
            SquareState.X if self.current_player == SquareState.O else SquareState.O
        )

    def _is_win(self):
        return any(
            [
                self.board[a] == self.board[b] == self.board[c]
                for a, b, c in WINNING_COMBOS
                if self.board[a] != SquareState.EMPTY
            ]
        )

    def get_available_moves(self):
        return [i for i, square in enumerate(self.board) if square == SquareState.EMPTY]

    def get_result(self):
        if self._is_win():
            return Result.X_WINS if self.current_player == SquareState.O else Result.O_WINS
        elif len(self.get_available_moves()) == 0:
            return Result.DRAW
        else:
            return Result.NOT_FINISHED
