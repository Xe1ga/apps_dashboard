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
def add_game_in_db(game_db, db_session):
    db_session.add(game_db)
    db_session.flush()
    yield
    db_session.query(Game).filter(Game.id == game_db.id).delete()
    db_session.flush()


@pytest.fixture(scope="function")
def add_review_in_db(db_session, add_game_in_db, review_db):
    game = db_session.query(Game).filter(Game.active.is_(True)).first()
    game.reviews.extend([review_db])
    db_session.flush()
    yield


@pytest.fixture(scope="function")
def reviews(review_entry):
    return [review_entry]
