from wargames.core.game_logic import Game, SquareState
import mock
import pytest

from wargames.core.gpt_player import GptPlayer, UnknownException


class StubGptClient:
    def __init__(self):
        self.messages = []

    def chat(self, message):
        return self.messages.pop(0)


def test_player_make_move_and_gpt_responds():
    game = Game()
    game.make_move(0)

    client = StubGptClient()
    gpt_player = GptPlayer(client)
    client.messages = [
        {'message':
             {'function_call':
                  {
                      'arguments': '{\n "chosen_number": "1"\n}'
                   }
              }
         }
    ]

    game.make_move(gpt_player.get_next_move(game.board))

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


def test_gpt_fails_to_respond():
    game = Game()
    game.make_move(0)

    client = mock.MagicMock()
    client.chat.side_effect = Exception("GPT failed to respond")
    gpt_player = GptPlayer(client)
    with pytest.raises(UnknownException):
        gpt_player.get_next_move(game.board)



def test_gpt_fails_to_respond_2():
    game = Game()
    game.make_move(0)

    client = mock.MagicMock()
    client.chat.return_value = {
        "message": {
            "function_call": {
                "arguments": "{\"chosen_number\": 1}"
            }
        }
    }
    gpt_player = GptPlayer(client)

    gpt_player.get_next_move(game.board)
    client.chat.assert_called_once()
