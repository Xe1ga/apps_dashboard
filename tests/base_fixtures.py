import pytest

from base.connect import engine, Base
from base.models import Game
from base.queries import create_session


@pytest.fixture(scope="session", autouse=True)
def base_meta_data():
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def add_game_in_db(get_games):
    with create_session() as session:
        session.add(get_games)
        yield
        session.query(Game).filter(Game.id == get_games.id).delete()
