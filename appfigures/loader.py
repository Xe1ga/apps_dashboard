#!/usr/bin/env python
# -*- coding: utf-8 -*-

from decimal import Decimal
from typing import Generator

from utils import str_to_date
from settings import GAMES, PRODUCTS_ENDPOINT, REVIEWS_ENDPOINT, PERIOD_DAYS, RECORDS_PER_PAGE
from appfigures.structure import GameEntry, ReviewEntry
from appfigures.httpclient import get_deserialize_response_data


def get_games_info() -> Generator:
    """
    Получить информацию об играх из appfigures
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
    for app_id_in_store in apps_id.split("|"):
        yield get_deserialize_response_data(PRODUCTS_ENDPOINT + f"{store}/{app_id_in_store}")


def get_reviews_info(app_id_in_appfigure: int) -> Generator:
    """
    Получить информацию о комментариях к игре
    :param app_id_in_appfigure:
    :return:
    """
    yield from map(lambda r: ReviewEntry(content=r.get("review"),
                                        author=r.get("author"),
                                        pub_date=str_to_date(r.get("date")),
                                        stars=float(r.get("stars"))
                                        ),
                   get_reviews_for_current_game(app_id_in_appfigure))


def get_reviews_for_current_game(app_id_in_appfigure: int) -> Generator:
    """
    Получить комментарии с appfigure по id игры
    :param app_id_in_appfigure:
    :return:
    """
    url = REVIEWS_ENDPOINT + str(app_id_in_appfigure)
    this_page = pages = 1
    while this_page <= pages:
        data = get_deserialize_response_data(
            url,
            page=this_page,
            count=RECORDS_PER_PAGE,
            start=-PERIOD_DAYS
        )
        print(data.get('reviews'))
        yield from data.get('reviews')
        pages = data.get('pages')
        this_page += 1
