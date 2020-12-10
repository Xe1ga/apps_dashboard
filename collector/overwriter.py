#!/usr/bin/env python
# -*- coding: utf-8 -*-

from settings import RECREATE_DB_SCHEMA
from base.queries import delete_all_games, add_games, add_reviews, recreate_database_schema


def start_overwriting_tables():
    """Запуск алгоритма полной перезаписи таблиц новыми данными за период"""
    recreate_database_schema() if RECREATE_DB_SCHEMA else delete_all_games()
    add_games()
    add_reviews(all_period=True)
