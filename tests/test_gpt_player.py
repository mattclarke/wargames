import os

import pytest

from wargames.core.gpt_player import GptPlayer, AuthenticationException, GptClient


def get_openai_info():
    filepath = os.path.join(os.path.dirname(__file__), "..", "..", "key.txt")
    with open(filepath, "r") as f:
        lines = f.readlines()
        key = lines[0].strip()
        org = lines[1].strip()
    return key, org


def test_can_ask_gpt_to_pick_random_number_from_list():
    client = GptClient(*get_openai_info())
    gpt = GptPlayer(client)
    result = gpt.get_next_move([1, 2, 3, 4, 5, 6, 7, 8, 9])
    assert result in [1, 2, 3, 4, 5, 6, 7, 8, 9]


def test_gets_correct_number_if_only_one_choice():
    client = GptClient(*get_openai_info())
    gpt = GptPlayer(client)
    result = gpt.get_next_move([1])
    assert result == 1


def test_raise_exception_if_invalid_api_info():
    client = GptClient("invalid_key", "invalid_org")
    gpt = GptPlayer(client)
    with pytest.raises(AuthenticationException):
        gpt.get_next_move([1, 2, 3, 4, 5, 6, 7, 8, 9])


