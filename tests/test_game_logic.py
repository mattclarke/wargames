from core.game_logic import Board, SquareState, Result
import pytest

from core.game_logic import InvalidMoveException


def create_board(state=None):
    if not state:
        return Board()

    board = Board()
    o_idx = [i for i, x in enumerate(state) if x == "O"]
    x_idx = [i for i, x in enumerate(state) if x == "X"]

    for i in range(len(o_idx) + len(x_idx)):
        if i % 2 == 0:
            board.make_move(o_idx.pop())
        else:
            board.make_move(x_idx.pop())

    return board


def test_empty_board_on_init():
    board = create_board()
    assert board.is_empty()


def test_that_first_move_is_o():
    board = create_board()
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
    board = create_board()
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
    board = create_board()
    board.make_move(0)
    with pytest.raises(InvalidMoveException):
        board.make_move(0)


def test_not_allowed_move_outside_of_create_board():
    board = create_board()
    with pytest.raises(InvalidMoveException):
        board.make_move(9)
    with pytest.raises(InvalidMoveException):
        board.make_move(-1)


def test_that_game_not_finished():
    board = create_board(
        ['O', 'O', '',
         'X', 'X', '',
         '', '', '']
    )
    assert board.get_result() == Result.NOT_FINISHED


def test_that_three_in_a_row_is_win():
    board = create_board(
        ['O', 'O', 'O',
         'X', 'X', '',
         '', '', '']
    )
    assert board.get_result() == Result.O_WINS


def test_that_three_in_a_col_is_win():
    board = create_board(
        ['', '', 'O',
         '', 'X', 'O',
         'X', '', 'O']
    )
    assert board.get_result() == Result.O_WINS


def test_that_three_in_a_diag_is_win():
    board = create_board(
        ['', 'X', 'O',
         '', 'O', 'X',
         'O', '', '']
    )
    assert board.get_result() == Result.O_WINS


def test_that_game_is_finished_after_winning():
    board = create_board(
        ['O', 'O', 'O',
         'X', 'X', '',
         '', '', '']
    )
    assert board.get_result() != Result.NOT_FINISHED


def test_that_game_is_draw_after_all_square_are_taken():
    board = create_board(
        ['O', 'X', 'O',
         'O', 'X', 'X',
         'X', 'O', 'O']
    )
    assert board.get_result() == Result.DRAW


def test_second_player_won_the_game():
    board = create_board(
        ['O', 'O', '',
         'X', 'X', 'X',
         '', '', 'O']
    )
    assert board.get_result() == Result.X_WINS
