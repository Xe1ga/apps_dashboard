#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import boto3
from botocore.exceptions import ClientError


def create_bucket(bucket_name, region=None):
    """
    Создает корзину
    :param bucket_name:
    :param region:
    :return:
    """
    try:
        if region is None:
            s3_client = boto3.client('s3')
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client = boto3.client('s3', region_name=region)
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name,
                                    CreateBucketConfiguration=location)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def is_exist_bucket(name_bucket: str) -> bool:
    """
    Проверка существования козины
    :param name_bucket:
    :return:
    """
    s3 = boto3.client('s3')
    response = s3.list_buckets()
    buckets = [bucket["Name"] for bucket in response['Buckets']]
    return name_bucket in buckets


def upload_file(file_name, bucket, object_name=None) -> bool:
    """
    Загружает файл в корзину и возвращает True при успехе, иначе False
    :param file_name:
    :param bucket:
    :param object_name:
    :return:
    """
    if object_name is None:
        object_name = file_name

    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True