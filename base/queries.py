#!/usr/bin/env python
# -*- coding: utf-8 -*-

from base.connect import engine, Base, Session


Base.metadata.create_all(engine)


def update_game_table():
    pass
