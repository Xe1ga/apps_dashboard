#!/usr/bin/env python
# -*- coding: utf-8 -*-

from appfigures.loader import get_games_info, get_reviews_info
from base.connect import engine, Base, Session
from base.models import Game, Review


Base.metadata.create_all(engine)


def delete_old_entries():
    session = Session()
    all_games = session.query(Game).all()
    for game in all_games:
        session.delete(game)
    session.commit()
    session.close()


def update_game_table():
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


def update_review_table():
    """Добавляет комментарии к играм"""

    session = Session()
    all_games = session.query(Game).all()
    for game in all_games:
        reviews = [Review(content=review_entry.content,
                          author=review_entry.author,
                          pub_date=review_entry.pub_date,
                          stars=review_entry.stars
                          )
                   for review_entry in get_reviews_info(game.app_id_in_appfigure)]
        game.reviews = reviews
        session.add(game)
    session.commit()
    session.close()

