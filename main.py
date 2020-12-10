#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from settings import OVERWRITE_TABLES
from appfigures.exceptions import TimeoutConnectionError, ConnectError, HTTPError
from collector.overwriter import start_overwriting_tables
from collector.updater import start_updating_tables


def setup_logger():
    logger = logging.getLogger("apps_dashboard")
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s:%(name)s:%(lineno)d:%(levelname)s:%(message)s')

    stream_handler = logging.StreamHandler()
    file_handler = logging.FileHandler('log/apps_dashboard.log')

    stream_handler.setLevel(logging.ERROR)
    file_handler.setLevel(logging.INFO)

    stream_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)

    return logger


logger = setup_logger()


def run():
    logger.info("Скрипт запущен")
    try:
        start_overwriting_tables() if OVERWRITE_TABLES else start_updating_tables()
    except (TimeoutConnectionError, ConnectError, HTTPError) as err:
        logger.error(f'При отправке HTTP запроса возникла ошибка: {err}')

    logger.info("Скрипт завершил работу")


if __name__ == "__main__":
    run()
