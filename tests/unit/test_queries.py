import pytest

from sqlalchemy.exc import SQLAlchemyError
from appfigures.exceptions import TimeoutConnectionError, ConnectError, HTTPError, DBError

from unittest.mock import patch, Mock

from base.queries import create_session, add_game_entry
from base.models import Game
from appfigures.structure import GameEntry


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


def test_add_game_entry(get_game_entry):
    with create_session() as session:
        add_game_entry(get_game_entry, session)
        games = session.query(Game).first()
        assert get_game_entry == GameEntry(
            app_id_in_appfigures=games.app_id_in_appfigures,
            app_id_in_store=games.app_id_in_store,
            game_name=games.game_name,
            id_store=games.id_store,
            store=games.store,
            icon_link_appfigures=games.icon_link_appfigures,
            icon_link_s3=games.icon_link_s3

        )
        session.query(Game).filter(Game.id == games.id).delete()
