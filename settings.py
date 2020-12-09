#!/usr/bin/env python
# -*- coding: utf-8 -*-

from envparse import env

from utils import calc_past_date


# Подключение к API
USERNAME = env.str('USERNAME_AF')

PASSWORD = env.str('PASSWORD')

APP_KEY = env.str('APP_KEY')

BASE_URL = env.str('BASE_URL')


# Параметры подключения к БД проекта
DB_ENGINE = env.str('DB_ENGINE')

DB_HOST = env.str('DB_HOST')

DB_NAME = env.str('DB_NAME')

DB_PORT = env.str('DB_PORT')

DB_USER = env.str('DB_USER')

DB_PASSWORD = env.str('DB_PASSWORD')


# Настройки проекта

# Словарь ключ-имя магазина, значения - строки, коды игр в данном магазине с разделителем "|"
GAMES = env('GAMES', cast=dict, subcast=str)

# Период хранения данных в БД в днях, по умолчанию - текущий день
PERIOD_DAYS = env.int('PERIOD_DAYS', default=0)

START_DATE = calc_past_date(PERIOD_DAYS)

RECORDS_PER_PAGE = env.int('RECORDS_PER_PAGE')

PRODUCTS_ENDPOINT = env.str('PRODUCTS_ENDPOINT')

REVIEWS_ENDPOINT = env.str('REVIEWS_ENDPOINT')

OVERWRITE_TABLES = env.bool('OVERWRITE_TABLES', default=True)

# Язык, на котором написан отзыв. Пример значения "en,ru", если переменная среды не определена ищем на всех языках.
PREDICTED_LANGUAGES = env('PREDICTED_LANGUAGES', cast=list, subcast=str, default=None)
