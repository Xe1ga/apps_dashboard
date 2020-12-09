#!/usr/bin/env python
# -*- coding: utf-8 -*-

from base.queries import delete_all_games, add_games, add_reviews


def start_overwriting_tables():
    delete_all_games()
    add_games()
    add_reviews(all_period=True)
