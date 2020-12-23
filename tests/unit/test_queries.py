import pytest

from unittest.mock import patch, Mock


@pytest.mark.parametrize('url, parameters, headers', request_attributes)
@patch('repository_statistics.httpclient._get_response')
def test_get_response_data_200_ok(mock_get_response, url, parameters, headers):
    """Тест на фугкцию get_response, когда возвращается статус 200 ОК"""
    response_return_value(mock_get_response)
    response_data = get_response_data(url, parameters, headers)
    assert response_data.response_json == result_json