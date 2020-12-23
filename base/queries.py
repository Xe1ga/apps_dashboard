#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError

from typing import Any, Iterator
from contextlib import contextmanager

from utils import get_values_list_from_dict, date_to_str_without_time, get_next_day
from settings import GAMES
from appfigures.structure import GameEntry
from appfigures.loader import get_reviews_info, get_one_game_info
from appfigures.exceptions import TimeoutConnectionError, ConnectError, HTTPError, DBError
from base.connect import engine, Base, Session
from base.models import Game, Review


Base.metadata.create_all(engine)


@contextmanager
def create_session(**kwargs: Any) -> Iterator[Session]:
    """
    Контекстный менеждер сессии
    :param kwargs:
    :return:
    """
    new_session = Session(**kwargs)
    try:
        yield new_session
        new_session.commit()
    except SQLAlchemyError as err:
        new_session.rollback()
        raise DBError(f'При выполнении операций с базой данных возникла ошибка. {err}')
    except (TimeoutConnectionError, ConnectError, HTTPError):
        new_session.rollback()
        raise
    finally:
        new_session.close()


def recreate_database_schema():
    """Удаление и создание таблиц БД"""
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def add_reviews():
    """Добавляет комментарии к играм"""

    with create_session() as session:
        all_games = session.query(Game).filter(Game.active.is_(True)).all()
        for game in all_games:
            reviews = [Review(id_in_appfigures=review_entry.id_in_appfigures,
                              content=review_entry.content,
                              author=review_entry.author,
                              pub_date=review_entry.pub_date,
                              stars=review_entry.stars
                              )
                       for review_entry in get_reviews_info(game, get_start_date(game.id, session))]

            game.reviews.extend(reviews)
            session.add(game)


def mark_inactive_games():
    """Отметить значение active = False у тех игр, которые не указаны в переменной окружения как активные"""
    with create_session() as session:
        session.query(Game).filter(Game.app_id_in_store.notin_(get_values_list_from_dict(GAMES))). \
            update({Game.active: False}, synchronize_session=False)


def select_game(store: str, app_id_in_store: str, session: Session):
    """
    Отбор записи о игре из таблицы игр
    :param store:
    :param app_id_in_store:
    :param session:
    :return:
    """
    game = session.query(Game).filter(Game.app_id_in_store == app_id_in_store, Game.store == store).first()
    return game


def add_game_entry(game_entry: GameEntry, session: Session):
    """
    Добавить запись об игре
    :param game_entry:
    :param session:
    :return:
    """
    game = Game(app_id_in_appfigures=game_entry.app_id_in_appfigures,
                app_id_in_store=game_entry.app_id_in_store,
                game_name=game_entry.game_name,
                id_store=game_entry.id_store,
                store=game_entry.store,
                icon_link_appfigures=game_entry.icon_link_appfigures,
                icon_link_s3=game_entry.icon_link_s3
                )
    session.add(game)


def get_start_date(game_id: str, session: Session) -> str:
    """
    Возвращает дату, с которой будет начинаться поиск комментариев
    :param game_id:
    :param session:
    :return:
    """
    last_date = session.query(func.max(Review.pub_date)). \
        filter(Review.game_id == game_id).group_by(Review.game_id).scalar()
    return date_to_str_without_time(get_next_day(last_date)) if last_date else None


def update_game_table():
    """Обновить таблицу игр, удалив лишние строки, добавив отсутствующие и обновив изменившиеся записи"""
    with create_session() as session:
        for store, apps_id in GAMES.items():
            for app_id_in_store in apps_id.split("|"):
                game_info_from_base = select_game(store, app_id_in_store, session)
                game_info_from_app = get_one_game_info(store, app_id_in_store)
                if game_info_from_base is None:
                    add_game_entry(game_info_from_app, session)
                else:
                    for field in game_info_from_app._fields:
                        setattr(game_info_from_base, field, getattr(game_info_from_app, field))
