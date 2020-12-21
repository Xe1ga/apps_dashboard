#!/usr/bin/env python
# -*- coding: utf-8 -*-

from decimal import Decimal
from typing import Generator, Optional
from datetime import datetime

from utils import str_to_date, is_common_elements_exist, date_to_str_without_time
from settings import GAMES, PRODUCTS_ENDPOINT, REVIEWS_ENDPOINT, START_DATE, RECORDS_PER_PAGE, PREDICTED_LANGUAGES
from appfigures.structure import GameEntry, ReviewEntry
from appfigures.httpclient import get_deserialize_response_data
from aws.s3client import transfer_image_and_return_link


def get_games_info() -> Generator:
    """
    Получить информацию об играх из appfigures
    :return:
    """
    for store, apps_id in GAMES.items():
        yield from map(lambda g: GameEntry(app_id_in_appfigures=g.get("id"),
                                           app_id_in_store=g.get("vendor_identifier"),
                                           game_name=g.get("name"),
                                           id_store=g.get("store_id"),
                                           store=g.get("store"),
                                           icon_link_appfigures=g.get("icon"),
                                           icon_link_s3=transfer_image_and_return_link(
                                                   app_id_in_appfigures=g.get("id"),
                                                   name=g.get("name"),
                                                   icon_link=g.get("icon")
                                               )
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


def get_reviews_info(app_id_in_appfigures: int, start: Optional[datetime] = START_DATE) -> Generator:
    """
    Получить информацию о комментариях к игре
    :param app_id_in_appfigures:
    :param start:
    :return:
    """
    yield from map(lambda r: ReviewEntry(id_in_appfigures=r.get("id"),
                                         content=r.get("review"),
                                         author=r.get("author"),
                                         pub_date=str_to_date(r.get("date")),
                                         stars=Decimal(r.get("stars"))
                                         ),
                   filter_by_language(get_reviews_for_current_game(app_id_in_appfigures, start))
                   if PREDICTED_LANGUAGES else get_reviews_for_current_game(app_id_in_appfigures, start))


def get_reviews_for_current_game(app_id_in_appfigures: int, start: Optional[datetime] = START_DATE) -> Generator:
    """
    Получить комментарии с appfigures по id игры
    :param app_id_in_appfigures:
    :param start:
    :return:
    """
    start_date = date_to_str_without_time(start)
    url = REVIEWS_ENDPOINT + str(app_id_in_appfigures)
    this_page = pages = 1
    while this_page <= pages:
        data = get_deserialize_response_data(
            url,
            page=this_page,
            count=RECORDS_PER_PAGE,
            start=start_date
        )
        yield from data.get('reviews')
        pages = data.get('pages')
        this_page += 1


def filter_by_language(reviews: Generator) -> Generator:
    """
    Возвращает отфильтрованные по языку комментарии
    :param reviews:
    :return:
    """
    yield from filter(lambda r: is_common_elements_exist(r.get("predicted_langs"), PREDICTED_LANGUAGES), reviews)


def get_one_game_info(store: str, app_id_in_store: str) -> GameEntry:
    """
    Получить информацию по конкретной игре
    :param store:
    :param app_id_in_store:
    :return:
    """
    g = get_deserialize_response_data(PRODUCTS_ENDPOINT + f"{store}/{app_id_in_store}")
    return GameEntry(app_id_in_appfigures=g.get("id"),
                     app_id_in_store=g.get("vendor_identifier"),
                     game_name=g.get("name"),
                     id_store=g.get("store_id"),
                     store=g.get("store"),
                     icon_link_appfigures=g.get("icon"),
                     icon_link_s3=transfer_image_and_return_link(
                             app_id_in_appfigures=g.get("id"),
                             name=g.get("name"),
                             icon_link=g.get("icon")
                         )
                     )
