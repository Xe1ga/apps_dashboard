#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import boto3

from botocore.exceptions import ClientError

from settings import LOCALSTACK_S3_ENDPOINT_URL, AWS_SECRET_ACCESS_KEY, AWS_ACCESS_KEY_ID, REGION
from aws.exceptions import S3ClientError


def get_client():
    if LOCALSTACK_S3_ENDPOINT_URL:
        client_config = {
            'service_name': 's3',
            'aws_access_key_id': AWS_ACCESS_KEY_ID,
            'aws_secret_access_key': AWS_SECRET_ACCESS_KEY,
            'endpoint_url': LOCALSTACK_S3_ENDPOINT_URL
        }
    else:
        client_config = {
            'service_name': 's3'
        }
    return client_config


def create_bucket(bucket_name):
    """
    Создает корзину
    :param bucket_name:
    :return:
    """
    client_config = get_client()
    try:
        if REGION is None:
            s3_client = boto3.client(**client_config)
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client = boto3.client(**client_config, region_name=REGION)
            location = {'LocationConstraint': REGION}
            s3_client.create_bucket(Bucket=bucket_name,
                                    CreateBucketConfiguration=location)
    except ClientError as err:
        raise S3ClientError(f'При создании s3 bucket возникла ошибка. {err}')
        return False
    return True


def is_exist_bucket(name_bucket: str) -> bool:
    """
    Проверка существования козины
    :param name_bucket:
    :return:
    """
    client_config = get_client()
    s3_client = boto3.client(**client_config)
    response = s3_client.list_buckets()
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

    client_config = get_client()
    s3_client = boto3.client(**client_config)

    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True
