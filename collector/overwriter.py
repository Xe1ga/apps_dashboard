#!/usr/bin/env python
# -*- coding: utf-8 -*-

from base.queries import delete_all_games, add_games, add_reviews
from appfigures.loader import get_games_info


def start_overwriting_tables():
    delete_all_games()
    add_games()
    add_reviews()
