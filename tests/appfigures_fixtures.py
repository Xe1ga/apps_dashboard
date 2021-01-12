import pytest

from settings import (GAME_SETTINGS, FILTER_BY_COUNTRIES, FILTER_BY_LANGS, FILTER_BY_PREDICTED_LANGS)


@pytest.fixture(scope="function")
def filter_by_countries(game_db):
    FILTER_BY_COUNTRIES.append(game_db.app_id_in_store)
    yield
    FILTER_BY_COUNTRIES.remove(game_db.app_id_in_store)


@pytest.fixture(scope="function")
def filter_by_langs(game_db):
    FILTER_BY_LANGS.append(game_db.app_id_in_store)
    yield
    FILTER_BY_LANGS.remove(game_db.app_id_in_store)


@pytest.fixture(scope="function")
def filter_by_predicted_langs(game_db):
    FILTER_BY_PREDICTED_LANGS.append(game_db.app_id_in_store)
    yield
    FILTER_BY_PREDICTED_LANGS.remove(game_db.app_id_in_store)


@pytest.fixture(scope="function")
def add_game_settings_for_langs_filter(game_db):
    GAME_SETTINGS[game_db.app_id_in_store] = {"store_name": "google_play", "langs": "gb,ru"}
    yield
    GAME_SETTINGS.pop(game_db.app_id_in_store)


@pytest.fixture(scope="function")
def add_game_settings_for_countries_filter(game_db):
    GAME_SETTINGS[game_db.app_id_in_store] = {"store_name": "apple", "langs": "GB,RU"}
    yield
    GAME_SETTINGS.pop(game_db.app_id_in_store)


@pytest.fixture(scope="function")
def add_game_settings(game_db):
    GAME_SETTINGS[game_db.app_id_in_store] = {"store_name": "apple"}
    yield
    GAME_SETTINGS.pop(game_db.app_id_in_store)


@pytest.fixture(scope="function")
def add_game_settings_for_post_filtration(game_db):
    GAME_SETTINGS[game_db.app_id_in_store] = {"store_name": "amazon_appstore", "langs": "ru"}
    yield
    GAME_SETTINGS.pop(game_db.app_id_in_store)
