import pytest

from typing import NamedTuple

from settings import FILTER_BY_COUNTRIES

pytest_plugins = ['appfigures_fixtures']

GAME_SETTINGS = {"com.playrix.zoo_m3.gplay": {"store_name": "google_play", "langs": "gb,ru"}, "B07TSDPQ42": {"store_name": "amazon_appstore", "langs": "en,ru"}, "664575829": {"store_name": "apple", "langs": "GB,RU"}}
