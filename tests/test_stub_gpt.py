class GptWrapper:
    pass


class StubGptWrapper:
    def __init__(self):
        self.messages = []

    def send(self, prompt):
        return self.messages.pop(0)


class Game:
    def __init__(self, client):
        self._client = client

    def _extract_squares(self, part):
        board = part.strip().replace("-", "").replace("\n\n", "|").replace(" ", "")
        return board.split("|")

    def extract_board(self, response):
        content = response["choices"][0]["message"]["content"].strip()
        parts = content.replace("```", "`").split("`")
        return [
            self._extract_squares(part)
            for idx, part in enumerate(parts)
            if idx % 2 == 1
        ]

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

        return self.extract_board(response)[-1]

    def move(self, position):
        response = self._client.send(f"I choose {position}")
        return self.extract_board(response)[-1]


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

    boards = Game(None).extract_board(new_game_response)

    assert boards[0] == ["1", "2", "3", "4", "5", "6", "7", "8", "9"]


def test_parse_initial_response_when_bot_goes_first():
    new_game_response = {
        "choices": [
            {
                "finish_reason": "stop",
                "index": 0,
                "message": {
                    "content": "Sure thing! \n\nHere's the initial board:\n\n```\n1 | 2 | 3  \n---------\n4 | 5 | 6 \n---------\n7 | 8 | 9\n```\n\nI'll start by placing an X in the center of the board (position 5):\n\n```\n1 | 2 | 3  \n---------\n4 | X | 6 \n---------\n7 | 8 | 9\n```\n\nYour turn, where would you like to put your O?",
                    "role": "assistant",
                },
            }
        ],
        "created": 1685704217,
        "id": "chatcmpl-7MwxdUK2s5EmQ1uS86YlqI0kLE9vU",
        "model": "gpt-3.5-turbo-0301",
        "object": "chat.completion",
        "usage": {"completion_tokens": 99, "prompt_tokens": 76, "total_tokens": 175},
    }

    boards = Game(None).extract_board(new_game_response)

    assert boards[0] == ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    assert boards[1] == ["1", "2", "3", "4", "X", "6", "7", "8", "9"]


def test_parse_move_response():
    response = {
        "choices": [
            {
                "finish_reason": "stop",
                "index": 0,
                "message": {
                    "content": "Okay, here's the updated board:\n\n```\n O | 2 | 3 \n-----------\n 4 | X | 6 \n-----------\n 7 | 8 | 9 \n```\n\nIt's now my turn, and I'll choose square number 3:\n\n```\n O | 2 | X\n-----------\n 4 | X | 6 \n-----------\n 7 | 8 | 9 \n```\n\nYour turn again, please choose a square to mark 'O'.",
                    "role": "assistant",
                },
            }
        ],
        "created": 1686227396,
        "id": "chatcmpl-7P940vbjKHVSpIbpVBtbIrLgttb17",
        "model": "gpt-3.5-turbo-0301",
        "object": "chat.completion",
        "usage": {"completion_tokens": 97, "prompt_tokens": 175, "total_tokens": 272},
    }

    boards = Game(None).extract_board(response)

    assert boards[0] == ["O", "2", "3", "4", "X", "6", "7", "8", "9"]
    assert boards[1] == ["O", "2", "X", "4", "X", "6", "7", "8", "9"]


def test_parse_when_we_win():
    response = {
        "choices": [
            {
                "finish_reason": "stop",
                "index": 0,
                "message": {
                    "content": "Okay, here's the updated board:\n\n```\n O | O | X\n-----------\n O | X | 6 \n-----------\n O | 8 | X \n```\n\nGreat move! You have three 'O's in a row and have won the game. Congratulations!",
                    "role": "assistant",
                },
            }
        ],
        "created": 1686228630,
        "id": "chatcmpl-7P9NuBAcIr9Th21TqCAcp6emdoNgZ",
        "model": "gpt-3.5-turbo-0301",
        "object": "chat.completion",
        "usage": {"completion_tokens": 54, "prompt_tokens": 542, "total_tokens": 596},
    }

    boards = Game(None).extract_board(response)

    assert boards[0] == ['O', 'O', 'X', 'O', 'X', '6', 'O', '8', 'X']


def test_asking_it_to_start_a_new_game_we_go_first():
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

    client = StubGptWrapper()
    client.messages.append(new_game_response)
    game = Game(client)
    current_board = game.start(player_first=True)

    assert current_board == ["1", "2", "3", "4", "5", "6", "7", "8", "9"]


def test_asking_it_to_start_a_new_game_bot_goes_first():
    new_game_response = {
        "choices": [
            {
                "finish_reason": "stop",
                "index": 0,
                "message": {
                    "content": "Sure thing! \n\nHere's the initial board:\n\n```\n1 | 2 | 3  \n---------\n4 | 5 | 6 \n---------\n7 | 8 | 9\n```\n\nI'll start by placing an X in the center of the board (position 5):\n\n```\n1 | 2 | 3  \n---------\n4 | X | 6 \n---------\n7 | 8 | 9\n```\n\nYour turn, where would you like to put your O?",
                    "role": "assistant",
                },
            }
        ],
        "created": 1685704217,
        "id": "chatcmpl-7MwxdUK2s5EmQ1uS86YlqI0kLE9vU",
        "model": "gpt-3.5-turbo-0301",
        "object": "chat.completion",
        "usage": {"completion_tokens": 99, "prompt_tokens": 76, "total_tokens": 175},
    }

    client = StubGptWrapper()
    client.messages.append(new_game_response)
    game = Game(client)
    current_board = game.start(player_first=False)

    assert current_board == ["1", "2", "3", "4", "X", "6", "7", "8", "9"]


def test_we_make_a_move_then_it_counters():
    responses = [
        {
            "choices": [
                {
                    "finish_reason": "stop",
                    "index": 0,
                    "message": {
                        "content": "Sure thing! \n\nHere's the initial board:\n\n```\n1 | 2 | 3  \n---------\n4 | 5 | 6 \n---------\n7 | 8 | 9\n```\n\nI'll start by placing an X in the center of the board (position 5):\n\n```\n1 | 2 | 3  \n---------\n4 | X | 6 \n---------\n7 | 8 | 9\n```\n\nYour turn, where would you like to put your O?",
                        "role": "assistant",
                    },
                }
            ],
            "created": 1685704217,
            "id": "chatcmpl-7MwxdUK2s5EmQ1uS86YlqI0kLE9vU",
            "model": "gpt-3.5-turbo-0301",
            "object": "chat.completion",
            "usage": {
                "completion_tokens": 99,
                "prompt_tokens": 76,
                "total_tokens": 175,
            },
        },
        {
            "choices": [
                {
                    "finish_reason": "stop",
                    "index": 0,
                    "message": {
                        "content": "Okay, here's the updated board:\n\n```\n O | 2 | 3 \n-----------\n 4 | X | 6 \n-----------\n 7 | 8 | 9 \n```\n\nIt's now my turn, and I'll choose square number 3:\n\n```\n O | 2 | X\n-----------\n 4 | X | 6 \n-----------\n 7 | 8 | 9 \n```\n\nYour turn again, please choose a square to mark 'O'.",
                        "role": "assistant",
                    },
                }
            ],
            "created": 1686227396,
            "id": "chatcmpl-7P940vbjKHVSpIbpVBtbIrLgttb17",
            "model": "gpt-3.5-turbo-0301",
            "object": "chat.completion",
            "usage": {
                "completion_tokens": 97,
                "prompt_tokens": 175,
                "total_tokens": 272,
            },
        },
    ]

    client = StubGptWrapper()
    client.messages = responses

    game = Game(client)
    _ = game.start(player_first=False)

    current_board = game.move("1")

    assert current_board == ["O", "2", "X", "4", "X", "6", "7", "8", "9"]


def test_we_win_the_game():
    pass
