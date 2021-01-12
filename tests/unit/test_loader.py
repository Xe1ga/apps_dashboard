import pytest

from unittest.mock import patch
from datetime import datetime

from settings import RECORDS_PER_PAGE
from utils import date_to_str_without_time
from appfigures.loader import (is_filter_by_countries, is_filter_by_langs, is_post_filtration_by_predicted_langs,
                               get_params, get_review, filter_by_language)


expected_result_with_date = {
        "page": 1,
        "count": RECORDS_PER_PAGE,
        "start": '2020-12-01',
        "end": date_to_str_without_time(datetime.now()),
    }

expected_result_without_date = {
        "page": 1,
        "count": RECORDS_PER_PAGE,
        "start": None,
        "end": date_to_str_without_time(datetime.now()),
    }

expected_result_countries_filter = {
        "page": 1,
        "count": RECORDS_PER_PAGE,
        "start": None,
        "end": date_to_str_without_time(datetime.now()),
        "countries": "GB,RU"
    }

expected_result_langs_filter = {
        "page": 1,
        "count": RECORDS_PER_PAGE,
        "start": None,
        "end": date_to_str_without_time(datetime.now()),
        "langs": "gb,ru"
    }


response_data = {"reviews": [{'author': 'author', 'title': 'title',
                              'review': 'review', 'original_title': 'original_title',
                              'original_review': 'original_review', 'stars': '5.00', 'iso': 'RU',
                              'version': None, 'date': '2020-12-26T18:07:08', 'deleted': False,
                              'has_response': False, 'product': 31599121121, 'product_id': 31599121121,
                              'product_name': 'product_name', 'vendor_id': '664575829',
                              'store': 'apple', 'weight': 0, 'id': 'id',
                              'predicted_langs': ['ru', 'uk']}],
                 "pages": 1}


response_data_en = {"reviews": [{'author': 'author', 'title': 'title',
                                 'review': 'review', 'original_title': 'original_title',
                                 'original_review': 'original_review', 'stars': '5.00', 'iso': 'RU',
                                 'version': None, 'date': '2020-12-26T18:07:08', 'deleted': False,
                                 'has_response': False, 'product': 31599121121, 'product_id': 31599121121,
                                 'product_name': 'product_name', 'vendor_id': '664575829',
                                 'store': 'apple', 'weight': 0, 'id': 'id',
                                 'predicted_langs': ['en']}],
                    "pages": 1}


def test_is_filter_by_countries_true(get_games, filter_by_countries):
    """Тест на функцию is_filter_by_countries, когда возвращается True"""
    assert is_filter_by_countries(get_games) is True


def test_is_filter_by_langs_true(get_games, filter_by_langs):
    """Тест на функцию is_filter_by_langs, когда возвращается True"""
    assert is_filter_by_langs(get_games) is True


def test_is_post_filtration_by_predicted_langs_true(get_games, filter_by_predicted_langs):
    """Тест на функцию is_filter_by_predicted_langs, когда возвращается True"""
    assert is_post_filtration_by_predicted_langs(get_games) is True


def test_is_filter_by_countries_false(get_games):
    """Тест на функцию is_filter_by_countries, когда возвращается False"""
    assert is_filter_by_countries(get_games) is False


def test_is_filter_by_langs_false(get_games):
    """Тест на функцию is_filter_by_langs, когда возвращается False"""
    assert is_filter_by_langs(get_games) is False


def test_is_post_filtration_by_predicted_langs_false(get_games):
    """Тест на функцию is_filter_by_predicted_langs, когда возвращается False"""
    assert is_post_filtration_by_predicted_langs(get_games) is False


@pytest.mark.usefixtures("add_game_settings")
@pytest.mark.parametrize('this_page,start,expected_result',
                         [(1, "2020-12-01", expected_result_with_date),
                          (1, None, expected_result_without_date)])
def test_get_params_without_filters(this_page, start, expected_result, get_games):
    """Тест на функцию get_params"""
    params = get_params(get_games, this_page, start)
    assert params == expected_result


@pytest.mark.usefixtures("add_game_settings_for_countries_filter", "filter_by_countries")
@pytest.mark.parametrize('this_page,start,expected_result',
                         [(1, None, expected_result_countries_filter)])
def test_get_params_without_filters(this_page, start, expected_result, get_games):
    """Тест на функцию get_params"""
    params = get_params(get_games, this_page, start)
    assert params == expected_result


@pytest.mark.usefixtures("add_game_settings_for_langs_filter", "filter_by_langs")
@pytest.mark.parametrize('this_page,start,expected_result',
                         [(1, None, expected_result_langs_filter)])
def test_get_params_without_filters(this_page, start, expected_result, get_games):
    """Тест на функцию get_params"""
    params = get_params(get_games, this_page, start)
    assert params == expected_result


def get_deserialize_response_data_return_value(mock_function):
    mock_function.return_value = response_data


@pytest.mark.usefixtures("add_game_settings")
@pytest.mark.parametrize('start', ["2020-12-01", None])
@patch('appfigures.loader.get_deserialize_response_data')
def test_get_deserialize_response_data_exception(mock_response_data, get_games, start):
    """Тест на фугкцию get_deserialize_response_data, когда возникают исключения при десериализации"""
    get_deserialize_response_data_return_value(mock_response_data)
    data = get_review(get_games, start)
    assert list(data) == response_data.get("reviews")


def get_reviews_gen(r):
    yield from r.get("reviews")


@pytest.mark.usefixtures("add_game_settings_for_post_filtration")
@pytest.mark.parametrize('reviews,expected_result',
                         [(get_reviews_gen(response_data), response_data.get("reviews")),
                          (get_reviews_gen(response_data_en), [])])
def test_filter_by_language(reviews, expected_result, get_games):

    filter_data = filter_by_language(reviews, get_games)
    assert list(filter_data) == expected_result
