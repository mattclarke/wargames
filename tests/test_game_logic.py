from core.game_logic import Game, SquareState, Result
import pytest

from core.game_logic import InvalidMoveException


def create_game(state=None):
    if not state:
        return Game()

    game = Game()
    o_idx = [i for i, x in enumerate(state) if x == "O"]
    x_idx = [i for i, x in enumerate(state) if x == "X"]

    for i in range(len(o_idx) + len(x_idx)):
        if i % 2 == 0:
            game.make_move(o_idx.pop())
        else:
            game.make_move(x_idx.pop())

    return game


def test_empty_board_on_init():
    game = create_game()
    assert game.board == [SquareState.EMPTY] * 9


def test_that_first_move_is_o():
    game = create_game()
    game.make_move(0)
    assert game.board == [
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
    game = create_game()
    game.make_move(0)
    game.make_move(1)
    assert game.board == [
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
    game = create_game()
    game.make_move(0)
    with pytest.raises(InvalidMoveException):
        game.make_move(0)


def test_not_allowed_move_outside_of_create_game():
    game = create_game()
    with pytest.raises(InvalidMoveException):
        game.make_move(9)
    with pytest.raises(InvalidMoveException):
        game.make_move(-1)


def test_that_game_not_finished():
    game = create_game(
        ['O', 'O', '',
         'X', 'X', '',
         '', '', '']
    )
    assert game.get_result() == Result.NOT_FINISHED


def test_that_three_in_a_row_is_win():
    game = create_game(
        ['O', 'O', 'O',
         'X', 'X', '',
         '', '', '']
    )
    assert game.get_result() == Result.O_WINS


def test_that_three_in_a_col_is_win():
    game = create_game(
        ['', '', 'O',
         '', 'X', 'O',
         'X', '', 'O']
    )
    assert game.get_result() == Result.O_WINS


def test_that_three_in_a_diag_is_win():
    game = create_game(
        ['', 'X', 'O',
         '', 'O', 'X',
         'O', '', '']
    )
    assert game.get_result() == Result.O_WINS


def test_that_game_is_finished_after_winning():
    game = create_game(
        ['O', 'O', 'O',
         'X', 'X', '',
         '', '', '']
    )
    assert game.get_result() != Result.NOT_FINISHED


def test_that_game_is_draw_after_all_square_are_taken():
    game = create_game(
        ['O', 'X', 'O',
         'O', 'X', 'X',
         'X', 'O', 'O']
    )
    assert game.get_result() == Result.DRAW


def test_second_player_won_the_game():
    game = create_game(
        ['O', 'O', '',
         'X', 'X', 'X',
         '', '', 'O']
    )
    assert game.get_result() == Result.X_WINS


def test_that_getting_board_is_not_mutating_class():
    game = create_game()
    board = game.board
    board[0] = SquareState.X
    assert game.board[0] == SquareState.EMPTY