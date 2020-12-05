#!/usr/bin/env python
# -*- coding: utf-8 -*-

from base.queries import update_game_table, delete_old_entries, update_review_table


def run():
    # delete_old_entries()
    update_game_table()
    update_review_table()


if __name__ == "__main__":
    run()
