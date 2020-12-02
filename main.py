#!/usr/bin/env python
# -*- coding: utf-8 -*-

from envparse import env

from appfigures.structure import ReportParams
from appfigures.httpclient import get_response_content_with_pagination, get_deserialize_response_data


report_params = ReportParams(
        username=env.str('USERNAME_AF'),
        password=env.str('PASSWORD'),
        app_key=env.str('APP_KEY'),
        base_url=env.str('BASE_URL'),
        period_days=env.int('PERIOD_DAYS'),
        records_per_page=env.int('RECORDS_PER_PAGE')

    )


def run():
    pass



if __name__ == "__main__":
    run()
