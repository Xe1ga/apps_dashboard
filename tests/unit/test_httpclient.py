import pytest

from unittest.mock import patch, Mock
from json.decoder import JSONDecodeError
from datetime import datetime, timedelta

from appfigures.httpclient import _get_response, get_deserialize_response_data, get_response_with_stream, requests
from appfigures.exceptions import TimeoutConnectionError, ConnectError, HTTPError


endpoint_url = "http://url"


params = {
    "page": 1,
    "count": 100,
    "start": datetime.now() - timedelta(days=1),
    "end": datetime.now(),
}


JSON_DATA = {"key1": "val1", "key2": "val2"}


request_attributes = [(endpoint_url, params)]


mock_status_200 = Mock(status_code=200, json={"created_at": "date", "author": {"login": "name"}})


def response_return_value(mock_function):
    mock_function.return_value.status_code = 200
    mock_function.return_value.json.return_value = JSON_DATA
    mock_function.return_value.links = {}
    mock_function.return_value.headers = {}


def raise_http_error():
    raise requests.exceptions.HTTPError(response=Mock(status_code=404))


def get_structure_response_data(*args, **kwargs):
    response_json = [JSON_DATA]
    return response_json


def response_return_value_with_json_exception(mock_function):
    mock_function.return_value.status_code = 200
    mock_function.return_value.json.side_effect = [ValueError, JSONDecodeError]
    mock_function.return_value.links = {}
    mock_function.return_value.headers = {}


@pytest.mark.parametrize('url, parameters', request_attributes)
@patch.object(requests, 'get')
def test_get_response_200_ok(mock_requests_get, url, parameters):
    """Тест на функцию _get_response, когда возвращается статус 200 ОК"""
    response_return_value(mock_requests_get)
    response = _get_response(url, parameters)
    assert response.json() == JSON_DATA


@pytest.mark.parametrize('url, parameters', request_attributes)
@patch.object(requests, 'get', side_effect=[requests.exceptions.Timeout(), requests.exceptions.ConnectionError()])
def test_get_response_timeout_connect_exception(mock_requests_get, url, parameters):
    """Тест на функцию _get_response, когда возникют исключения Timeout, ConnectionError"""
    with pytest.raises(TimeoutConnectionError):
        _get_response(url, parameters)
    with pytest.raises(ConnectError):
        _get_response(url, parameters)


@pytest.mark.parametrize('url, parameters', request_attributes)
@patch.object(requests, 'get', return_value=Mock(status_code=404))
def test_get_response_http_exception(mock_requests_get, url, parameters):
    """Тест на фугкцию get_response, когда возникют исключения HTTPError"""
    mock_requests_get.return_value.status_code = 404
    mock_requests_get.return_value.raise_for_status.side_effect = raise_http_error
    with pytest.raises(HTTPError):
        _get_response(url, parameters)


@pytest.mark.parametrize('url, parameters', request_attributes)
def test_get_deserialize_response_data(url, parameters):
    """Тест get_deserialize_response_data при успешном выполнении"""
    with patch('appfigures.httpclient._get_response') as mock_get_response_data:
        mock_get_response_data.return_value.json.side_effect = get_structure_response_data
        response_json = get_deserialize_response_data(url, **parameters)
        assert response_json == [JSON_DATA]


@pytest.mark.parametrize('url, parameters', request_attributes)
@patch('appfigures.httpclient._get_response')
def test_get_deserialize_response_data_exception(mock_get_response, url, parameters):
    """Тест на фугкцию get_deserialize_response_data, когда возникают исключения при десериализации"""
    response_return_value_with_json_exception(mock_get_response)
    response_json = get_deserialize_response_data(url, **parameters)
    assert response_json is None


@pytest.mark.parametrize('url', [endpoint_url])
@patch.object(requests, 'get')
def test_get_response_with_stream_200_ok(mock_requests_get, url):
    """Тест на функцию get_response_with_stream, когда возвращается статус 200 ОК"""
    response_return_value(mock_requests_get)
    response = get_response_with_stream(url)
    assert response.json() == JSON_DATA


@pytest.mark.parametrize('url', [endpoint_url])
@patch.object(requests, 'get', return_value=Mock(status_code=404))
def test_get_response_http_exception(mock_requests_get, url):
    """Тест на функцию get_response_with_stream, когда возникют исключения HTTPError"""
    mock_requests_get.return_value.status_code = 404
    mock_requests_get.return_value.raise_for_status.side_effect = raise_http_error
    with pytest.raises(HTTPError):
        get_response_with_stream(url)
