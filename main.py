#!/usr/bin/env python
# -*- coding: utf-8 -*-

from settings import OVERWRITE_TABLES
from base.queries import update_game_table, delete_old_entries, update_review_table


def start_overwriting_tables():
    delete_old_entries()
    update_game_table()
    update_review_table()


def start_updating_tables():
    pass


def run():
    start_overwriting_tables() if OVERWRITE_TABLES else start_updating_tables()


if __name__ == "__main__":
    run()
