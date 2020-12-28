#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta


def str_to_date(value: str) -> datetime:
    """
    Конвертирует строку формата ISO YYYY-MM-DDTHH:MM:SS из json в datetime
    :param value:
    :return:
    """
    return datetime.fromisoformat(value)


def date_to_str(value: datetime) -> str:
    """
    Конвертирует datetime в строку ISO формата YYYY-MM-DDTHH:MM:SS
    :param value:
    :return:
    """
    return datetime.isoformat(value)


def date_to_str_without_time(value: datetime) -> str:
    """
    Конвертирует datetime в строку  формата YYYY-MM-DD
    :param value:
    :return:
    """
    return value.strftime("%Y-%m-%d")


def is_common_elements_exist(l1: list, l2: list) -> bool:
    """
    Вернуть True, если списки имеют общие элементы и False, если не имеют
    :param l1:
    :param l2:
    :return:
    """
    return bool(set(l1) & set(l2))


def calc_past_date(value: int) -> datetime:
    """
    Вычислить дату в прошлом, за value дней до текущей даты
    :param value:
    :return:
    """
    return datetime.now() - timedelta(days=value)


def get_next_day(value: datetime) -> datetime:
    """
    Вернуть следующий день
    :param value:
    :return:
    """
    return value + timedelta(days=1)


def get_game_review_langs(game_setting: dict) -> list:
    """
    Вернуть список языков комментариев к текущей игре, указаны в настройках
    :param game_setting:
    :return:
    """
    langs = game_setting.get("langs")
    if langs:
        return langs.replace(" ", "").split(",")
    return []
