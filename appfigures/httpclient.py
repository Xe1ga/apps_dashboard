#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests

from typing import Generator
from json.decoder import JSONDecodeError

from appfigures.exceptions import TimeoutConnectionError, ConnectError, HTTPError

from settings import USERNAME, APP_KEY, PASSWORD, BASE_URL, RECORDS_PER_PAGE


def _get_response(url: str, querystring_params: dict) -> requests.Response:
    """
    Получить объект ответа requests.Response
    :param url:
    :param querystring_params:
    :return:
    """
    headers = {"X-Client-Key": APP_KEY}
    auth = (USERNAME, PASSWORD)
    http_error_codes = {
        400: "Один из параметров в запросе неверен или недействителен."
             " Проверьте тело для получения дополнительной информации.",
        401: "Не прошла авторизация. Проверьте корректность учетных данных.",
        403: "Доступ к ресурсу ограничен.",
        404: "Запрашиваемый ресурс не найден. Проверьте корректность url.",
        420: "Превышение количества разрешенных запросов за день."
    }

    try:
        response = requests.get(BASE_URL + url.lstrip("/"),
                                auth=auth,
                                params=querystring_params,
                                headers=headers)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        raise TimeoutConnectionError("Превышен таймаут получения ответа от сервера.")
    except requests.exceptions.ConnectionError:
        raise ConnectError("Проблема соединения с сервером.")
    except requests.exceptions.HTTPError as err:
        raise HTTPError(
            http_error_codes.get(
                err.response.status_code,
                f"Возникла HTTP ошибка, код ошибки: {err.response.status_code}."
            )
        )
    return response


def get_deserialize_response_data(url: str, **querystring_params) -> dict:
    """
    Получить десериализованные данные ответа Response и часть необходимых заголовков
    :param url:
    :param querystring_params:
    :return:
    """
    response = _get_response(url, querystring_params)

    try:
        response_json = response.json()
    except (ValueError, JSONDecodeError):
        response_json = None

    return response_json


def get_response_content_with_pagination(url: str) -> Generator:
    """
    Формирует генератор объектов поиска постранично
    :param url:
    :return:
    """
    this_page = pages = 1
    while this_page <= pages:
        data = get_deserialize_response_data(
            url,
            page=this_page,
            count=RECORDS_PER_PAGE
            )
        yield data.get('reviews')
        pages = data.get('pages')
        this_page += 1
