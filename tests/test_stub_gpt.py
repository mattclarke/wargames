class GptWrapper:
    pass


class StubGptWrapper:
    def __init__(self):
        self.messages = []

    def send(prompt):
        return self.messages.pop(0)


class Game:
    def __init__(self, client):
        self._client = client

    def extract_board(self, response):
        content = response["choices"][0]["message"]["content"].strip()
        parts = content.replace("```", "`").split("`")
        board = parts[1].strip().replace("\n---------\n", " | ").replace(" ", "")
        board = board.split("|")
        return board

    def start(self, player_first):
        if player_first:
            response = self._client.send(
                "Play some tic-tac-toe with me."
                "To represent the board we use the number 1-9,"
                "where 1 is the top left corner and 9 is the bottom right corner."
                "You play is X and i play as O. I go first"
            )
        else:
            response = self._client.send(
                "Play some tic-tac-toe with me."
                "To represent the board we use the number 1-9,"
                "where 1 is the top left corner and 9 is the bottom right corner."
                "You play is X and i play as O. You go first"
            )
        # TODO: parse response

        return [None] * 9


def test_parse_initial_response_when_we_go_first():
    new_game_response = {
        "choices": [
            {
                "finish_reason": "stop",
                "index": 0,
                "message": {
                    "content": "Sure, I'll go ahead and play with you. Here's the board:\n\n```\n1 | 2 | 3\n---------\n4 | 5 | 6\n---------\n7 | 8 | 9\n```\n\nOK, your move first. Which number would you like to place your 'O' in?",
                    "role": "assistant",
                },
            }
        ],
        "created": 1685704835,
        "id": "chatcmpl-7Mx7btPzM9im7tTUaqZMhnurz8o5e",
        "model": "gpt-3.5-turbo-0301",
        "object": "chat.completion",
        "usage": {"completion_tokens": 65, "prompt_tokens": 76, "total_tokens": 141},
    }

    board = Game(None).extract_board(new_game_response)

    assert board == ["1", "2", "3", "4", "5", "6", "7", "8", "9"]


#
# def test_asking_it_to_start_a_new_game():
#     # Ask to start a game and we go first
#     new_game_response = {
#         "choices": [
#             {
#                 "finish_reason": "stop",
#                 "index": 0,
#                 "message": {
#                     "content": "Sure, I'll go ahead and play with you. Here's the board:\n\n```\n1 | 2 | 3\n---------\n4 | 5 | 6\n---------\n7 | 8 | 9\n```\n\nOK, your move first. Which number would you like to place your 'O' in?",
#                     "role": "assistant",
#                 },
#             }
#         ],
#         "created": 1685704835,
#         "id": "chatcmpl-7Mx7btPzM9im7tTUaqZMhnurz8o5e",
#         "model": "gpt-3.5-turbo-0301",
#         "object": "chat.completion",
#         "usage": {"completion_tokens": 65, "prompt_tokens": 76, "total_tokens": 141},
#     }
#
#     client = StubGptWrapper()
#     client.messages.append(new_game_response)
#     game = Game(client)
#     current_board = game.start(player_first=True)
#
#     assert current_board == [None] * 9
#
#
# def test_new_game_bot_goes_first():
#     game = Game()
#     current_board = game.start(player_first=False)
#
#     assert current_board == [None] * 9
