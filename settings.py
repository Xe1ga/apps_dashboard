#!/usr/bin/env python
# -*- coding: utf-8 -*-

from envparse import env


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

# Пересоздать схему БД заново перед выполнением скрипта (удалить и создать таблицы)
RECREATE_DB_SCHEMA = env.bool('RECREATE_DB_SCHEMA', default=False)

RECORDS_PER_PAGE = env.int('RECORDS_PER_PAGE')

PRODUCTS_ENDPOINT = env.str('PRODUCTS_ENDPOINT')

REVIEWS_ENDPOINT = env.str('REVIEWS_ENDPOINT')

# Язык, на котором написан отзыв. Пример значения "en,ru", если переменная среды не определена ищем на всех языках.
PREDICTED_LANGUAGES = env('PREDICTED_LANGUAGES', cast=list, subcast=str, default=None)
# endpoint корзины s3
LOCALSTACK_S3_ENDPOINT_URL = env.str('LOCALSTACK_S3_ENDPOINT_URL')

AWS_ACCESS_KEY_ID = env.str('AWS_ACCESS_KEY_ID')

AWS_SECRET_ACCESS_KEY = env.str('AWS_SECRET_ACCESS_KEY')

REGION = env.str('REGION')

BUCKET = env.str('BUCKET')
