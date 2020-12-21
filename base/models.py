#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import ForeignKey, Column, Integer, SmallInteger, String, Text, DateTime, BigInteger, Numeric
from sqlalchemy.orm import relationship

from base.connect import Base


class Review(Base):
    __tablename__ = 'review'

    id = Column(BigInteger, primary_key=True)
    id_in_appfigures = Column(String(100), nullable=False, unique=True)
    content = Column(Text)
    author = Column(String(100), nullable=False)
    pub_date = Column(DateTime, nullable=False)
    stars = Column(Numeric(3, 2))
    game_id = Column(Integer, ForeignKey('game.id', ondelete='CASCADE'))

    game = relationship("Game", back_populates="reviews")

    def __repr__(self):
        return f"<Review({self.author}, {self.content})>"


class Game(Base):
    __tablename__ = 'game'

    id = Column(Integer, primary_key=True)
    app_id_in_appfigures = Column(BigInteger, nullable=False, unique=True)
    app_id_in_store = Column(String(50), nullable=False)
    game_name = Column(String(50), nullable=False)
    id_store = Column(SmallInteger, nullable=False)
    store = Column(String(50), nullable=False)
    icon_link_appfigures = Column(String(2048))
    icon_link_s3 = Column(String(2048))

    reviews = relationship("Review", back_populates="game", order_by="Review.pub_date",
                           cascade="all, delete, delete-orphan", passive_deletes=True)

    def __repr__(self):
        return f"<Game({self.app_id_in_appfigures}, {self.game_name})>"
