#!/usr/bin/env python
# -*- coding: utf-8 -*-

from decimal import Decimal
from typing import Generator, Optional
from datetime import datetime, timedelta

from utils import str_to_date, is_common_elements_exist, date_to_str_without_time
from settings import PRODUCTS_ENDPOINT, REVIEWS_ENDPOINT, RECORDS_PER_PAGE, PREDICTED_LANGS, LANGS, COUNTRIES
from appfigures.structure import GameEntry, ReviewEntry
from appfigures.httpclient import get_deserialize_response_data
from aws.s3client import transfer_image_and_return_link
from base.models import Game


def get_game_entry(g: dict) -> GameEntry:
    """
    Возвращает данные об игре в структуре GameEntry
    :param g: 
    :return: 
    """""
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


def is_need_select_by_langs_apple(game: Game) -> bool:
    """
    Определяет необходимость отбора комментариев по стране в параметре запроса для приложений на apple store
    :param game:
    :return:
    """
    return COUNTRIES is not None and game.id_store == 1


def is_need_select_by_langs_google(game: Game) -> bool:
    """
    Определяет необходимость отбора по языку в параметре запроса для приложений на google_play store
    :param game:
    :return:
    """
    return LANGS is not None and game.id_store == 2


def is_need_select_by_langs_amazon(game: Game) -> bool:
    """
    Определяет необходимость пост сортировки по языку для amazon
    :param game:
    :return:
    """
    return PREDICTED_LANGS is not None and game.id_store == 3


def get_reviews_info(game: Game, start: Optional[str]) -> Generator:
    """
    Получить информацию о комментариях к игре
    :param game:
    :param start:
    :return:
    """
    yield from map(lambda r: ReviewEntry(id_in_appfigures=r.get("id"),
                                         content=r.get("review"),
                                         author=r.get("author"),
                                         pub_date=str_to_date(r.get("date")),
                                         stars=Decimal(r.get("stars"))
                                         ),
                   filter_by_language(get_review(game, start))
                   if is_need_select_by_langs_amazon(game) else get_review(game, start))


def get_params(game: Game, this_page: int, start: Optional[str]) -> dict:
    """
    Возвращает словарь с параметрами для запроса по комментариям
    :param game:
    :param this_page:
    :param start:
    :return:
    """
    params = {
        "page": this_page,
        "count": RECORDS_PER_PAGE,
        "start": start,
        "end": date_to_str_without_time(datetime.now()),
    }
    if is_need_select_by_langs_apple(game):
        params["countries"] = COUNTRIES
    elif is_need_select_by_langs_google(game):
        params["langs"] = LANGS

    return params


def get_review(game: Game, start: Optional[str]) -> Generator:
    """
    Получить комментарии с appfigures по id игры
    :param game:
    :param start:
    :return:
    """
    url = REVIEWS_ENDPOINT + str(game.app_id_in_appfigures)
    this_page = pages = 1

    while this_page <= pages:
        params = get_params(game, this_page, start)
        data = get_deserialize_response_data(
            url,
            **params
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
    yield from filter(lambda r: is_common_elements_exist(r.get("predicted_langs"), PREDICTED_LANGS), reviews)


def get_one_game_info(store: str, app_id_in_store: str) -> GameEntry:
    """
    Получить информацию по конкретной игре
    :param store:
    :param app_id_in_store:
    :return:
    """
    g = get_deserialize_response_data(PRODUCTS_ENDPOINT + f"{store}/{app_id_in_store}")
    return get_game_entry(g)
