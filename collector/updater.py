#!/usr/bin/env python
# -*- coding: utf-8 -*-

from settings import START_DATE
from base.queries import delete_untracked_games, to_analyze_game_table, add_reviews


def start_updating_tables():
    """Запуск алгоритма добавления новых записей и удаления неактуальных записей из таблиц БД"""
    delete_untracked_games()
    to_analyze_game_table()
    add_reviews()
