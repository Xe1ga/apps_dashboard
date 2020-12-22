#!/usr/bin/env python
# -*- coding: utf-8 -*-

import boto3

from typing import Optional
from botocore.exceptions import ClientError, BotoCoreError

from settings import LOCALSTACK_S3_ENDPOINT_URL, AWS_SECRET_ACCESS_KEY, AWS_ACCESS_KEY_ID, REGION, BUCKET
from aws.exceptions import S3ClientError, Boto3CoreError
from appfigures.httpclient import get_response


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


def create_bucket(bucket_name: Optional[str] = BUCKET):
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


def is_exist_bucket(bucket_name: Optional[str] = BUCKET) -> bool:
    """
    Проверка существования козины
    :param bucket_name:
    :return:
    """
    client_config = get_client()
    try:
        s3_client = boto3.client(**client_config)
        response = s3_client.list_buckets()
        buckets = [bucket["Name"] for bucket in response['Buckets']]
    except BotoCoreError as err:
        raise Boto3CoreError(f'Ошибка создания клиента s3. Проверьте доступность ресурса. {err}')

    return bucket_name in buckets


def upload_fileobj(data: str, object_name: str, bucket: Optional[str] = BUCKET) -> str:
    """
    Загружает файл в корзину и возвращает url файла при успехе, иначе пустачя строка
    :param data:
    :param object_name:
    :param bucket:
    :return:
    """
    client_config = get_client()
    s3_client = boto3.client(**client_config)

    try:
        s3_client.upload_fileobj(data, bucket, object_name)
    except ClientError as err:
        raise S3ClientError(f'При загруке файла в s3 bucket возникла ошибка: {err}')
        return ""

    endpoint_url = s3_client.meta.endpoint_url.split("/")[2]
    return f"http://{bucket}.{endpoint_url}/{object_name}"


def download_file(object_name: str, file_name: str, bucket: Optional[str] = BUCKET):
    """
    Загрузить файл из корзины
    :param bucket:
    :param object_name:
    :param file_name:
    :return:
    """
    client_config = get_client()
    s3_client = boto3.client(**client_config)
    s3_client.download_file(bucket, object_name, file_name)


def transfer_image_and_return_link(app_id_in_appfigures: int, name: str, icon_link: str) -> str:
    """
    Загружает файл в s3 bucket и возвращает ссылку на него
    :param app_id_in_appfigures:
    :param name:
    :param icon_link:
    :return:
    """
    response = get_response(icon_link)
    object_name = name + str(app_id_in_appfigures) + "." + response.headers.get('Content-Type').split("/")[1]
    file_url = upload_fileobj(response.raw, object_name)
    return file_url
