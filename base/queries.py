#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import and_, func
from typing import Union, Generator

from utils import get_values_list_from_dict
from settings import GAMES
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


def add_reviews():
    """Добавляет комментарии к играм"""
    session = Session()
    all_games = session.query(Game).all()
    for game in all_games:
        reviews = [Review(id_in_appfigure=review_entry.id_in_appfigure,
                          content=review_entry.content,
                          author=review_entry.author,
                          pub_date=review_entry.pub_date,
                          stars=review_entry.stars
                          )
                   for review_entry in get_reviews_info(game.app_id_in_appfigure)]
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
    game = session.query(Game).filter(and_(Game.app_id_in_store == app_id_in_store, Game.store == store)).first()
    return game


def update_game(game_info_from_app: GameEntry, game_info_from_base: Game):
    """
    Обновить информацию об игре
    :param game_info_from_app:
    :param game_info_from_base:
    :return:
    """
    game_info_from_base.app_id_in_store = game_info_from_app.app_id_in_store
    game_info_from_base.app_id_in_appfigure = game_info_from_app.app_id_in_appfigure
    game_info_from_base.game_name = game_info_from_app.game_name
    game_info_from_base.id_store = game_info_from_app.id_store
    game_info_from_base.store = game_info_from_app.store
    game_info_from_base.icon_link = game_info_from_app.icon_link


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
                    update_game(game_info_from_app, game_info_from_base)
    session.commit()
    session.close()


def to_analyze_review_table():
    """Анализировать таблицу комментариев к играм, добавив недостающие комментарии"""
    session = Session()
    all_games = session.query(Game).all()
    for game in all_games:
        last_date = session.query(func.max(Review.pub_date)).filter(Review.game_id == game.id).group_by(Review.game_id)
        print(last_date)
        # reviews = [Review(content=review_entry.content,
        #                   author=review_entry.author,
        #                   pub_date=review_entry.pub_date,
        #                   stars=review_entry.stars
        #                   )
        #            for review_entry in get_reviews_info(game.app_id_in_appfigure)]
        # game.reviews = reviews
        # session.add(game)
    session.commit()
    session.close()
