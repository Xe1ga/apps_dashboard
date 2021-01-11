import pytest

from base.connect import engine, Base
from base.models import Game
from base.queries import create_session


@pytest.fixture(scope="function")
def db_session():
    with create_session() as session:
        yield session


@pytest.fixture(scope="session", autouse=True)
def base_meta_data():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def add_game_in_db(get_games, db_session):
    db_session.add(get_games)
    db_session.flush()
    yield
    db_session.query(Game).filter(Game.id == get_games.id).delete()
    db_session.flush()


@pytest.fixture(scope="function")
def reviews(get_review_entry):
    return [get_review_entry]
