import pytest

from settings import (GAME_SETTINGS, FILTER_BY_COUNTRIES, FILTER_BY_LANGS, FILTER_BY_PREDICTED_LANGS)


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


@pytest.fixture(scope="function")
def add_game_settings_for_post_filtration(get_games):
    GAME_SETTINGS[get_games.app_id_in_store] = {"store_name": "amazon_appstore", "langs": "ru"}
    yield
    GAME_SETTINGS.pop(get_games.app_id_in_store)
