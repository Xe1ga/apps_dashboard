import pytest

from sqlalchemy.exc import SQLAlchemyError
from appfigures.exceptions import TimeoutConnectionError, ConnectError, HTTPError, DBError

from unittest.mock import patch, Mock

from base.queries import create_session, add_game_entry, add_reviews
from base.models import Game, Review
from appfigures.structure import GameEntry, ReviewEntry


def mock_session_side_effect():
    return [SQLAlchemyError, TimeoutConnectionError(""), ConnectError(""), HTTPError("")]


@patch("base.queries.Session")
def test_create_session(mock_session):
    mock_session.return_value.commit.side_effect = mock_session_side_effect()
    with pytest.raises(DBError):
        with create_session() as session:
            pass
    mock_session.return_value.rollback.assert_called()

    with pytest.raises(TimeoutConnectionError):
        with create_session() as session:
            pass
    mock_session.return_value.rollback.assert_called()

    with pytest.raises(ConnectError):
        with create_session() as session:
            pass
    mock_session.return_value.rollback.assert_called()

    with pytest.raises(HTTPError):
        with create_session() as session:
            pass
    mock_session.return_value.rollback.assert_called()


def test_add_game_entry(get_game_entry, db_session):
    add_game_entry(get_game_entry, db_session)
    games = db_session.query(Game).first()

    assert get_game_entry == GameEntry(
        app_id_in_appfigures=games.app_id_in_appfigures,
        app_id_in_store=games.app_id_in_store,
        game_name=games.game_name,
        id_store=games.id_store,
        store=games.store,
        icon_link_appfigures=games.icon_link_appfigures,
        icon_link_s3=games.icon_link_s3

    )
    db_session.query(Game).filter(Game.id == games.id).delete()


@patch("base.queries.get_reviews_info")
def test_add_reviews(mock_reviews_info, db_session, get_games, add_game_in_db, reviews):
    mock_reviews_info.return_value = reviews
    add_reviews(db_session)

    review = db_session.query(Review).filter(Review.game_id == get_games.id).first()
    assert reviews[0] == ReviewEntry(
        id_in_appfigures=review.id_in_appfigures,
        content=review.content,
        author=review.author,
        pub_date=review.pub_date,
        stars=review.stars
    )

