#!/usr/bin/env python
# -*- coding: utf-8 -*-

from settings import OVERWRITE_TABLES
from collector.overwriter import start_overwriting_tables
from collector.updater import start_updating_tables


def run():
    start_overwriting_tables() if OVERWRITE_TABLES else start_updating_tables()


if __name__ == "__main__":
    run()
