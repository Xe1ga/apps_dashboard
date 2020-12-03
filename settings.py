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
PERIOD_DAYS = env.int('PERIOD_DAYS')
RECORDS_PER_PAGE = env.int('RECORDS_PER_PAGE')
