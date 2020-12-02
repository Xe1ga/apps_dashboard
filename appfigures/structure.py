# -*- coding: utf-8 -*-

"""
Модуль содержит структуры данных, используемые в проекте
"""

from typing import NamedTuple, Optional


class ReportParams(NamedTuple):
    """Параметры отчета"""
    username: str
    password: str
    app_key: str
    base_url: str
    period_days: int
    records_per_page: int
