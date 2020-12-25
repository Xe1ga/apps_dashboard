import pytest

from typing import NamedTuple

from settings import FILTER_BY_COUNTRIES


class Game(NamedTuple):
    """Запись об игре"""
    app_id_in_store: str


@pytest.fixture()
def game_entry():
    game_id = FILTER_BY_COUNTRIES[0]
    return Game(app_id_in_store=game_id)
