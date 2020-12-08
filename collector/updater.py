#!/usr/bin/env python
# -*- coding: utf-8 -*-

from base.queries import delete_untracked_games, to_analyze_review_table, to_analyze_game_table


def start_updating_tables():
    delete_untracked_games()
    to_analyze_game_table()
    to_analyze_review_table()
