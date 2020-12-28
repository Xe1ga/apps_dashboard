import pytest

from base.models import Game

pytest_plugins = ['appfigures_fixtures']

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
