from core.game_logic import Board, SquareState, Result
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


def test_that_game_not_finished():
    board = Board()
    board.make_move(0)
    board.make_move(3)
    board.make_move(1)
    board.make_move(4)
    assert board.get_result() == Result.NOT_FINISHED


def test_that_three_in_a_row_is_win():
    board = Board()
    board.make_move(0)
    board.make_move(3)
    board.make_move(1)
    board.make_move(4)
    board.make_move(2)
    assert board.get_result() != Result.DRAW

def test_that_three_in_a_col_is_win():
    board = Board()
    board.make_move(2)
    board.make_move(4)
    board.make_move(5)
    board.make_move(6)
    board.make_move(8)
    assert board.get_result() != Result.DRAW


def test_that_three_in_a_diag_is_win():
    board = Board()
    board.make_move(2)
    board.make_move(0)
    board.make_move(4)
    board.make_move(8)
    board.make_move(6)
    assert board.get_result() != Result.DRAW


def test_that_game_is_finished_after_winning():
    board = Board()
    board.make_move(2)
    board.make_move(0)
    board.make_move(4)
    board.make_move(8)
    board.make_move(6)
    assert board.get_result() != Result.NOT_FINISHED


def test_that_game_is_draw_after_all_square_are_taken():
    board = Board()
    board.make_move(0)
    board.make_move(4)
    board.make_move(2)
    board.make_move(1)
    board.make_move(7)
    board.make_move(6)
    board.make_move(5)
    board.make_move(8)
    board.make_move(3)
    assert board.get_result() == Result.DRAW


def test_first_player_won_the_game():
    board = Board()
    board.make_move(2)
    board.make_move(0)
    board.make_move(4)
    board.make_move(8)
    board.make_move(6)
    assert board.get_result() == Result.O


def test_second_player_won_the_game():
    board = Board()
    board.make_move(7)
    board.make_move(2)
    board.make_move(0)
    board.make_move(4)
    board.make_move(8)
    board.make_move(6)
    assert board.get_result() == Result.X


def test_get_result_when_game_is_not_finished():
    board = Board()
    board.make_move(7)
    board.make_move(2)
    board.make_move(0)
    board.make_move(4)
    board.make_move(8)
    assert board.get_result() == Result.NOT_FINISHED


