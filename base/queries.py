#!/usr/bin/env python
# -*- coding: utf-8 -*-

from appfigures.structure import GameEntry
from appfigures.loader import get_games_info
from base.connect import engine, Base, Session
from base.models import Game


Base.metadata.create_all(engine)


def update_game_table():
    """В рамках одной сессии добавляет информацию об играх в таблицу игр"""

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
