#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime

from base.queries import delete_untracked_games, to_analyze_game_table, add_reviews, delete_old_reviews


def start_updating_tables():
    """Запуск алгоритма добавления новых записей и удаления неактуальных записей из таблиц БД"""
    delete_untracked_games()
    to_analyze_game_table()
    delete_old_reviews()
    add_reviews(all_period=False)
