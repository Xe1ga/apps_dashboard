import pytest

from unittest.mock import patch, Mock

from appfigures.loader import is_filter_by_countries, is_filter_by_langs, is_post_filtration_by_predicted_langs


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
