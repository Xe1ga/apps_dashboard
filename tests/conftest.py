import pytest

from datetime import datetime

from appfigures.structure import GameEntry, ReviewEntry
from base.models import Game


pytest_plugins = ['appfigures_fixtures', 'base_fixtures']

GAME_SETTINGS = {"com.playrix.zoo_m3.gplay": {"store_name": "google_play", "langs": "gb,ru"}, "B07TSDPQ42": {"store_name": "amazon_appstore", "langs": "en,ru"}, "664575829": {"store_name": "apple", "langs": "GB,RU"}}


@pytest.fixture(scope="function")
def get_games():
    """Фикстура игры"""
    game = Game(
        id=1,
        app_id_in_appfigures=333,
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
def get_game_entry():
    """Фикстура игры"""
    game = GameEntry(
        app_id_in_appfigures=333,
        app_id_in_store="id_game_in_store",
        game_name="game name",
        id_store=1,
        store="store name",
        icon_link_appfigures="http://",
        icon_link_s3="http://s3"
    )
    return game


@pytest.fixture(scope="function")
def get_review_entry():
    review_entry = ReviewEntry(
        id_in_appfigures="256",
        content="review",
        author="author",
        pub_date=datetime.now(),
        stars=5
        )
    return review_entry
