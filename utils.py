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


def get_values_list_from_dict(d: dict) -> list:
    """
    Получить список значений словаря, для случая когда values - строки с разделителями |
    :param d:
    :return:
    """
    return "|".join(list(d.values())).split("|")


def calc_past_date(value: int) -> datetime:
    """
    Вычислить дату в прошлом, за value дней до текущей даты
    :param value:
    :return:
    """
    past_date = datetime.now() - timedelta(days=value)
    return past_date


def get_min_time_in_date(value: datetime) -> str:
    """
    Возвращает дату с минимальным временем
    :param value:
    :return:
    """
    return value.combine(value.date(), value.min.time())


def get_max_time_in_date(value: datetime) -> str:
    """
    Возвращает дату с максимальным временем
    :param value:
    :return:
    """
    return value.combine(value.date(), value.max.time())
