import pytest

from unittest.mock import patch, Mock
from typing import NamedTuple

from settings import FILTER_BY_COUNTRIES, FILTER_BY_LANGS, FILTER_BY_PREDICTED_LANGS
from appfigures.loader import is_filter_by_countries, is_filter_by_langs, is_post_filtration_by_predicted_langs


class Game(NamedTuple):
    """Запись об игре"""
    app_id_in_store: str


def get_games_with_filter(games_with_filter):
    return [Game(app_id_in_store=game_id) for game_id in games_with_filter]


@pytest.mark.parametrize('game', get_games_with_filter(FILTER_BY_COUNTRIES))
def test_is_filter_by_countries_true(game):
    """Тест на функцию is_filter_by_countries, когда возвращается True"""
    assert is_filter_by_countries(game) is True


@pytest.mark.parametrize('game', get_games_with_filter(FILTER_BY_LANGS))
def test_is_filter_by_langs_true(game):
    """Тест на функцию is_filter_by_countries, когда возвращается True"""
    assert is_filter_by_langs(game) is True


@pytest.mark.parametrize('game', get_games_with_filter(FILTER_BY_PREDICTED_LANGS))
def test_is_post_filtration_by_predicted_langs_true(game):
    """Тест на функцию is_filter_by_countries, когда возвращается True"""
    assert is_post_filtration_by_predicted_langs(game) is True
