#!/usr/bin/env python
# -*- coding: utf-8 -*-
import io
import logging

from settings import OVERWRITE_TABLES
from appfigures.exceptions import TimeoutConnectionError, ConnectError, HTTPError, DBError
from aws.exceptions import S3ClientError
from aws.s3client import create_bucket, upload_fileobj, download_file, is_exist_bucket
from collector.overwriter import start_overwriting_tables
from collector.updater import start_updating_tables


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
        start_overwriting_tables() if OVERWRITE_TABLES else start_updating_tables()
    except (TimeoutConnectionError, ConnectError, HTTPError, DBError, S3ClientError) as err:
        logger.error(f'Во время работы скрипта произошла ошибка: {err}')

    logger.info("Скрипт завершил работу")



    # import requests
    #
    # URL = 'https://play-lh.googleusercontent.com/83UIBGDsUeiJDR0bZPxT4xai5iqKXj6-3V6Snrqq3suXDSapL93Vf_fP6tJL5qEjEoM7=s180-rw'
    # filename = 'game1'
    # r = requests.get(URL, stream=True)
    # # upload_fileobj(io.BytesIO(r.content), "game-icons", filename + "." + r.headers.get('Content-Type').split("/")[1])
    # upload_fileobj(r.raw, filename + "." + r.headers.get('Content-Type').split("/")[1])
    #
    #
    #
    # # with open(filename + "." + r.headers.get('Content-Type').split("/")[1], 'wb') as fd:
    # #     upload_fileobj(r.content, "game-logo", filename + "." + r.headers.get('Content-Type').split("/")[1])
    #     # for chunk in r.iter_content(chunk_size=10000):
    #     #     fd.write(chunk)
    #
    # download_file("game1.webp", "gamenew1.webp")


if __name__ == "__main__":
    run()
