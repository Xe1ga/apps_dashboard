#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from settings import RECREATE_DB_SCHEMA
from appfigures.exceptions import TimeoutConnectionError, ConnectError, HTTPError, DBError
from aws.exceptions import S3ClientError, Boto3CoreError
from aws.s3client import create_bucket, is_exist_bucket
from base.queries import recreate_database_schema, mark_inactive_games, update_game_table, add_reviews


def setup_logger():
    logger = logging.getLogger("apps_dashboard")
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s:%(name)s:%(filename)s:%(lineno)d:%(levelname)s:%(message)s')

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
        if not is_exist_bucket():
            create_bucket()
        recreate_database_schema() if RECREATE_DB_SCHEMA else mark_inactive_games()
        update_game_table()
        add_reviews()
    except (TimeoutConnectionError, ConnectError, HTTPError, DBError, S3ClientError, Boto3CoreError) as err:
        logger.error(f'Во время работы скрипта произошла ошибка: {err}')

    logger.info("Скрипт завершил работу")


if __name__ == "__main__":
    run()
