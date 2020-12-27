#!/usr/bin/env python
# -*- coding: utf-8 -*-

from decimal import Decimal
from typing import Generator, Optional
from datetime import datetime

from utils import str_to_date, is_common_elements_exist, date_to_str_without_time, get_game_review_langs
from settings import (PRODUCTS_ENDPOINT, REVIEWS_ENDPOINT, RECORDS_PER_PAGE, FILTER_BY_COUNTRIES, FILTER_BY_LANGS,
                      FILTER_BY_PREDICTED_LANGS, GAME_SETTINGS)
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


def is_filter_by_countries(game: Game) -> bool:
    """
    Определяет необходимость отбора комментариев по стране в параметре запроса
    :param game:
    :return:
    """
    return game.app_id_in_store in FILTER_BY_COUNTRIES if FILTER_BY_COUNTRIES else False


def is_filter_by_langs(game: Game) -> bool:
    """
    Определяет необходимость отбора по языку в параметре запроса для приложений
    :param game:
    :return:
    """
    return game.app_id_in_store in FILTER_BY_LANGS if FILTER_BY_LANGS else False


def is_post_filtration_by_predicted_langs(game: Game) -> bool:
    """
    Определяет необходимость пост сортировки по языку
    :param game:
    :return:
    """
    return game.app_id_in_store in FILTER_BY_PREDICTED_LANGS if FILTER_BY_PREDICTED_LANGS else False


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
                   filter_by_language(get_review(game, start), game)
                   if is_post_filtration_by_predicted_langs(game) else get_review(game, start))


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

    langs = GAME_SETTINGS.get(game.app_id_in_store).get("langs")

    if langs:
        if is_filter_by_countries(game):
            params["countries"] = langs.replace(" ", "")
        elif is_filter_by_langs(game):
            params["langs"] = langs.replace(" ", "")

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


def filter_by_language(reviews: Generator, game: Game) -> Generator:
    """
    Возвращает отфильтрованные по языку комментарии
    :param reviews:
    :param game:
    :return:
    """
    yield from filter(lambda r: is_common_elements_exist(r.get("predicted_langs"),
                                                         get_game_review_langs(GAME_SETTINGS[game.app_id_in_store])),
                      reviews)


def get_one_game_info(store: str, app_id_in_store: str) -> GameEntry:
    """
    Получить информацию по конкретной игре
    :param store:
    :param app_id_in_store:
    :return:
    """
    g = get_deserialize_response_data(PRODUCTS_ENDPOINT + f"{store}/{app_id_in_store}")
    return get_game_entry(g)
