#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль содержит структуры данных, используемые в проекте
"""

from typing import NamedTuple, Optional
from datetime import datetime
from base.models import Game


class GameEntry(NamedTuple):
    """Запись об игре в БД"""
    app_id_in_appfigures: int
    app_id_in_store: str
    game_name: str
    id_store: int
    store: str
    icon_link_appfigures: Optional[str]
    icon_link_s3: Optional[str]


class ReviewEntry(NamedTuple):
    """Комментарий к игре"""
    id_in_appfigures: str
    content: str
    author: str
    pub_date: datetime
    stars: float
