#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime


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


def is_common_elements_exist(l1: list, l2: list) -> bool:
    return bool(set(l1) & set(l2))

