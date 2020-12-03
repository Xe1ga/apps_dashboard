#!/usr/bin/env python
# -*- coding: utf-8 -*-

from settings import GAMES, PRODUCTS_ENDPOINT
from base.queries import update_game_table
from structure import GameEntry
from httpclient import get_deserialize_response_data


def get_games_info():
    """
    Обновить таблицу продуктов (игр) из appfigures
    :return:
    """
    for store, apps_id in GAMES.items():
        update_game_table(map(lambda g: select_item_for_game_entry(g), get_game_info_from_appfigure(store, apps_id)))


def get_game_info_from_appfigure(store: str, apps_id: str) -> dict:
    """
    Получить данные об одной игре
    :param store:
    :param apps_id:
    :return:
    """
    for id in apps_id.split("|"):
        yield get_deserialize_response_data(PRODUCTS_ENDPOINT + f"{store}/{id}")


def select_item_for_game_entry(g: dict) -> GameEntry:
    """
    Отбирает необходимые данные для записи в таблицу Game
    :param g:
    :return:
    """
    return GameEntry(app_id_in_appfigure=g.get("id"),
                     app_id_in_store=g.get("vendor_identifier"),
                     game_name=g.get("name"),
                     id_store=g.get("store_id"),
                     store=g.get("store"),
                     icon=g.get("icon")
                     )
