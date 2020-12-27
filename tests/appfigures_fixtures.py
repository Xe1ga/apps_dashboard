import pytest

from datetime import datetime

from settings import (GAME_SETTINGS, FILTER_BY_COUNTRIES, FILTER_BY_LANGS, FILTER_BY_PREDICTED_LANGS, RECORDS_PER_PAGE)
from base.models import Game
from utils import date_to_str_without_time


@pytest.fixture(scope="function")
def get_games():
    """Фикстура игры"""
    game = Game(
        id=1,
        app_id_in_appfigures=3232323,
        app_id_in_store="id_game_in_store",
        game_name="game name",
        id_store=1,
        store="store name",
        icon_link_appfigures="http://",
        icon_link_s3="http://s3",
        active=1
    )
    return game


@pytest.fixture(scope="function")
def filter_by_countries(get_games):
    FILTER_BY_COUNTRIES.append(get_games.app_id_in_store)
    yield
    FILTER_BY_COUNTRIES.remove(get_games.app_id_in_store)


@pytest.fixture(scope="function")
def filter_by_langs(get_games):
    FILTER_BY_LANGS.append(get_games.app_id_in_store)
    yield
    FILTER_BY_LANGS.remove(get_games.app_id_in_store)


@pytest.fixture(scope="function")
def filter_by_predicted_langs(get_games):
    FILTER_BY_PREDICTED_LANGS.append(get_games.app_id_in_store)
    yield
    FILTER_BY_PREDICTED_LANGS.remove(get_games.app_id_in_store)


@pytest.fixture(scope="function")
def add_game_settings_for_langs_filter(get_games):
    GAME_SETTINGS[get_games.app_id_in_store] = {"store_name": "google_play", "langs": "gb,ru"}
    yield
    GAME_SETTINGS.pop(get_games.app_id_in_store)


@pytest.fixture(scope="function")
def add_game_settings_for_countries_filter(get_games):
    GAME_SETTINGS[get_games.app_id_in_store] = {"store_name": "apple", "langs": "GB,RU"}
    yield
    GAME_SETTINGS.pop(get_games.app_id_in_store)


@pytest.fixture(scope="function")
def add_game_settings(get_games):
    GAME_SETTINGS[get_games.app_id_in_store] = {"store_name": "apple"}
    yield
    GAME_SETTINGS.pop(get_games.app_id_in_store)
