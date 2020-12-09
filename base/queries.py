#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import func

from datetime import datetime
from typing import Optional

from utils import get_values_list_from_dict, date_to_str_without_time
from settings import GAMES, PERIOD_DAYS, START_DATE
from appfigures.structure import get_game_entry_structure, GameEntry
from appfigures.loader import get_reviews_info, get_one_game_info, get_games_info
from base.connect import engine, Base, Session
from base.models import Game, Review


Base.metadata.create_all(engine)


def delete_all_games():
    """Очистка таблицы игр"""
    session = Session()
    all_games = session.query(Game).all()
    for game in all_games:
        session.delete(game)
    session.commit()
    session.close()


def add_games():
    """Добавляет информацию об играх"""
    session = Session()
    all_games = [Game(app_id_in_appfigure=game_entry.app_id_in_appfigure,
                      app_id_in_store=game_entry.app_id_in_store,
                      game_name=game_entry.game_name,
                      id_store=game_entry.id_store,
                      store=game_entry.store,
                      icon_link=game_entry.icon_link
                      )
                 for game_entry in get_games_info()]
    session.add_all(all_games)
    session.commit()
    session.close()


def add_reviews(all_period: Optional[bool] = True):
    """
    Добавляет комментарии к играм
    :param all_period:
    :return:
    """
    session = Session()
    all_games = session.query(Game).all()
    for game in all_games:
        reviews = [Review(id_in_appfigure=review_entry.id_in_appfigure,
                          content=review_entry.content,
                          author=review_entry.author,
                          pub_date=review_entry.pub_date,
                          stars=review_entry.stars
                          )
                   for review_entry in get_reviews_info(game.app_id_in_appfigure,
                                                        START_DATE if all_period
                                                        else get_last_date_entry(game.id, session))]
        game.reviews = reviews
        session.add(game)
    session.commit()
    session.close()


def delete_untracked_games():
    """Удалить из таблицы игр записи об играх, которые не указаны в переменной окружения"""
    session = Session()
    session.query(Game).filter(
        Game.app_id_in_store.notin_(get_values_list_from_dict(GAMES))
    ).delete(synchronize_session=False)
    session.commit()
    session.close()


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
    Добавить одну запись об игре
    :param game_entry:
    :param session:
    :return:
    """
    game = Game(app_id_in_appfigure=game_entry.app_id_in_appfigure,
                app_id_in_store=game_entry.app_id_in_store,
                game_name=game_entry.game_name,
                id_store=game_entry.id_store,
                store=game_entry.store,
                icon_link=game_entry.icon_link
                )
    session.add(game)


def get_last_date_entry(id: str, session: Session) -> datetime:
    """
    Возвращает дату, с которой будет начинаться поиск комментариев
    :param id:
    :param session:
    :return:
    """
    last_date = session.query(func.max(Review.pub_date)). \
        filter(Review.game_id == id).group_by(Review.game_id).scalar()
    if last_date is not None and last_date > START_DATE:
        return last_date
    return START_DATE


def to_analyze_game_table():
    """Анализировать таблицу игр, удалив лишние строки, добавив отсутствующие и обновив изменившиеся записи"""
    session = Session()
    for store, apps_id in GAMES.items():
        for app_id_in_store in apps_id.split("|"):
            game_info_from_base = select_game(store, app_id_in_store, session)
            game_info_from_app = get_one_game_info(store, app_id_in_store)
            if game_info_from_base is None:
                add_game_entry(game_info_from_app, session)
            else:
                if get_game_entry_structure(game_info_from_base) != game_info_from_app:
                    for field in game_info_from_app._fields:
                        setattr(game_info_from_base, field, getattr(game_info_from_app, field))
    session.commit()
    session.close()


def delete_old_reviews():
    """Удалить все комментарии меньше START_DATE, включая START_DATE"""
    session = Session()
    session.query(Review).filter(Review.pub_date <= START_DATE).delete(synchronize_session=False)
    session.commit()
    session.close()
