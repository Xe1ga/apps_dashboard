#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Generator

from settings import GAMES, PRODUCTS_ENDPOINT
from appfigures.structure import GameEntry
from appfigures.httpclient import get_deserialize_response_data


def get_games_info():
    """
    Обновить таблицу продуктов (игр) из appfigures
    :return:
    """

    for store, apps_id in GAMES.items():
        yield from map(lambda g: GameEntry(app_id_in_appfigure=g.get("id"),
                                           app_id_in_store=g.get("vendor_identifier"),
                                           game_name=g.get("name"),
                                           id_store=g.get("store_id"),
                                           store=g.get("store"),
                                           icon_link=g.get("icon")
                                           ),
                       get_games_info_in_current_store(store, apps_id))


def get_games_info_in_current_store(store: str, apps_id: str) -> Generator:
    """
    Получить данные о всех играх одного магазина
    :param store:
    :param apps_id:
    :return:
    """
    for id in apps_id.split("|"):
        yield get_deserialize_response_data(PRODUCTS_ENDPOINT + f"{store}/{id}")
