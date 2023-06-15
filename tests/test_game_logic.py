from core.game_logic import Board






def test_empty_board_on_init():
    board = Board()
    assert board.is_empty()

def test_that_first_move_is_o():
    board = Board()
    board.make_move(0)
    assert board.board == ["O", "", "", "", "", "", "", "", ""]

def test_second_move_is_x():
    board = Board()
    board.make_move(0)
    board.make_move(1)
    assert board.board == ["O", "X", "", "", "", "", "", "", ""]





