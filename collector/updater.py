#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime

from base.queries import delete_untracked_games, to_analyze_game_table, add_reviews, delete_old_reviews, delete_reviews_on_period


def start_updating_tables():
    # delete_reviews_on_period(start=datetime(2020, 12, 10).date())
    delete_untracked_games()
    to_analyze_game_table()
    delete_old_reviews()
    add_reviews(all_period=False)
