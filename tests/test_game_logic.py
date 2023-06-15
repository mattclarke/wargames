from core.game_logic import Board, SquareState
import pytest

from core.game_logic import InvalidMoveException


def test_empty_board_on_init():
    board = Board()
    assert board.is_empty()


def test_that_first_move_is_o():
    board = Board()
    board.make_move(0)
    assert board.board == [
        SquareState.O,
        SquareState.EMPTY,
        SquareState.EMPTY,
        SquareState.EMPTY,
        SquareState.EMPTY,
        SquareState.EMPTY,
        SquareState.EMPTY,
        SquareState.EMPTY,
        SquareState.EMPTY,
    ]


def test_second_move_is_x():
    board = Board()
    board.make_move(0)
    board.make_move(1)
    assert board.board == [
        SquareState.O,
        SquareState.X,
        SquareState.EMPTY,
        SquareState.EMPTY,
        SquareState.EMPTY,
        SquareState.EMPTY,
        SquareState.EMPTY,
        SquareState.EMPTY,
        SquareState.EMPTY,
    ]


def test_not_allowed_move_to_same_square():
    board = Board()
    board.make_move(0)
    with pytest.raises(InvalidMoveException):
        board.make_move(0)


def test_not_allowed_move_outside_of_board():
    board = Board()
    with pytest.raises(InvalidMoveException):
        board.make_move(9)

    with pytest.raises(InvalidMoveException):
        board.make_move(-1)


