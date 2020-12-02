#!/usr/bin/env python
# -*- coding: utf-8 -*-

from envparse import env

from structure import ReportParams


def run():
    report_params = ReportParams(
        username=env.str('USERNAMEAF'),
        password=env.str('PASSWORD'),
        app_key=env.str('APP_KEY'),
        base_url=env.str('BASE_URL'),
        period_days=env.int('PERIOD_DAYS')

    )


if __name__ == "__main__":
    run()
