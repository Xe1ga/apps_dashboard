#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль содержит структуры данных, используемые в проекте
"""

from typing import NamedTuple, Optional
from datetime import datetime


class GameEntry(NamedTuple):
    """Запись об игре в БД"""
    app_id_in_appfigure: int
    app_id_in_store: str
    game_name: str
    id_store: int
    store: str
    icon_link: Optional[str]
