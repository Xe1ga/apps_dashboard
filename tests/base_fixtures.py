import pytest
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import sessionmaker

from settings import DB_ENGINE, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME


connection_string = f'{DB_ENGINE}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
engine = create_engine(connection_string)
Session = sessionmaker(bind=engine)

Base = declarative_base()


@pytest.fixture(scope='session')
def connection_string():
    """
    Строка подключения к тестовой БД
    """
    return f'{DB_ENGINE}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'


@pytest.fixture()
def postgres_engine(postgres):
    engine = create_engine(postgres, echo=True)
    try:
        yield engine
    finally:
        engine.dispose()


@pytest.fixture
def postgres(connection_string):
    """
    Создание пустой тестовой БД
    """
    Base.metadata.create_all(engine)
    with tmp_database(pg_url, 'pytest') as tmp_url:
        yield tmp_url
    Base.metadata.drop_all(engine)
