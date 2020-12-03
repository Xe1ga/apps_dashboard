#!/usr/bin/env python
# -*- coding: utf-8 -*-

from envparse import env

from appfigures.httpclient import get_response_content_with_pagination, get_deserialize_response_data

from settings import USERNAME
from base.connect import connection_string

def run():
    print(connection_string)


if __name__ == "__main__":
    run()
