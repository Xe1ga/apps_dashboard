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
    app_id_in_appfigure: int
    app_id_in_store: str
    game_name: str
    id_store: int
    store: str
    icon_link: Optional[str]


class ReviewEntry(NamedTuple):
    """Комментарий к игре"""
    id_in_appfigure: str
    content: str
    author: str
    pub_date: datetime
    stars: float


def get_game_entry_structure(data: Game):
    return GameEntry(
        app_id_in_appfigure=data.app_id_in_appfigure,
        app_id_in_store=data.app_id_in_store,
        game_name=data.game_name,
        id_store=data.id_store,
        store=data.store,
        icon_link=data.icon_link
    )
