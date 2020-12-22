# -*- coding: utf-8 -*-

"""
Модуль содержит собственные исключения модуля aws
"""


class Error(Exception):
    """
    Базовое исключение
    """
    def __init__(self, message):
        self.message = message


class S3ClientError(Error):
    """
    Исключение, возникающее при работе boto3 с S3 bucket
    """
    pass


class Boto3CoreError(Error):
    """
    Базовое исключение при работе boto3
    """
    pass
