# -*- coding: utf-8 -*-
from sqlalchemy import ForeignKey, Column, Integer, SmallInteger, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class Review(Base):
    __tablename__ = 'review'

    id = Column(Integer, primary_key=True)
    content = Column(Text)
    author = Column(String(50), nullable=False)
    pub_date = Column(DateTime, nullable=False)
    stars = Column(SmallInteger)
    game_id = Column(Integer, ForeignKey('game.id'))

    game = relationship("Game", back_populates="review")

    def __repr__(self):
        return f"<Review({self.author}, {self.content})>"


class Game(Base):
    __tablename__ = 'game'

    id = Column(Integer, primary_key=True)
    app_id_in_appfigure = Column(SmallInteger, nullable=False)
    app_id_in_store = Column(String(50), nullable=False)
    game_name = Column(String(50), nullable=False)
    id_store = Column(SmallInteger, nullable=False)
    store = Column(String(50), nullable=False)
    icon_link = Column(String(2048))

    review = relationship("Review", back_populates="game")

    def __repr__(self):
        return f"<Game({self.app_id_in_appfigure}, {self.game_name})>"
