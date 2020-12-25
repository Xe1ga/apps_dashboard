#!/usr/bin/env python
# -*- coding: utf-8 -*-

from envparse import env

env.read_envfile()

# Подключение к API appfigures
USERNAME = env.str('USERNAME_AF')

PASSWORD = env.str('PASSWORD')

APP_KEY = env.str('APP_KEY')

BASE_URL = env.str('BASE_URL')

RECORDS_PER_PAGE = env.int('RECORDS_PER_PAGE')

PRODUCTS_ENDPOINT = env.str('PRODUCTS_ENDPOINT')

REVIEWS_ENDPOINT = env.str('REVIEWS_ENDPOINT')


# Параметры подключения к БД проекта
DB_ENGINE = env.str('DB_ENGINE')

DB_HOST = env.str('DB_HOST')

DB_NAME = env.str('DB_NAME')

DB_PORT = env.str('DB_PORT')

DB_USER = env.str('DB_USER')

DB_PASSWORD = env.str('DB_PASSWORD')


# S3 bucket
# endpoint корзины s3
LOCALSTACK_S3_ENDPOINT_URL = env.str('LOCALSTACK_S3_ENDPOINT_URL')

AWS_ACCESS_KEY_ID = env.str('AWS_ACCESS_KEY_ID')

AWS_SECRET_ACCESS_KEY = env.str('AWS_SECRET_ACCESS_KEY')

REGION = env.str('REGION')

BUCKET = env.str('BUCKET')


# Настройки проекта

# Список из словарей - информация об игре: id игры в store, имя store, языки для фильтрации комментариев
GAME_SETTINGS = env.json('GAME_SETTINGS')

# Список игр, по которым необходима фильтрация по языку комментария после request запроса
FILTER_BY_PREDICTED_LANGS = env('FILTER_BY_PREDICTED_LANGS', cast=list, subcast=str, default=None)

# Список игр, по которым необходима фильтрация по языку комментария по параметру COUNTRIES в запросе
FILTER_BY_COUNTRIES = env('FILTER_BY_COUNTRIES', cast=list, subcast=str, default=None)

# Список игр, по которым необходима фильтрация по языку комментария по параметру LANGS в запросе
FILTER_BY_LANGS = env('FILTER_BY_LANGS', cast=list, subcast=str, default=None)

# Пересоздать схему БД заново перед выполнением скрипта (удалить и создать таблицы)
RECREATE_DB_SCHEMA = env.bool('RECREATE_DB_SCHEMA', default=False)

