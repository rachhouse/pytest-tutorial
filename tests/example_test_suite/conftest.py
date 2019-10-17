import json
import pytest
import re
import requests

BASE_URL = 'https://swapi.co/api'

SWAPI_RESOURCE_REGEX = re.compile(re.escape(BASE_URL) + r"\/(\w+)\/(\d+)\/*$")
SWAPI_RESOURCE_SCHEMA_REGEX = re.compile(re.escape(BASE_URL) + r"\/(\w+)\/*$")
SWAPI_BASE_REGEX = re.compile(re.escape(BASE_URL))

SWAPI_RESOURCES = ['films', 'people', 'planets', 'species', 'starships', 'vehicles']


class MockSwapiResponse:
    '''Mocks a HTTP response object from swapi'''

    def __init__(self, request_url: str) -> None:
        if SWAPI_BASE_REGEX.match(request_url):
            self.status_code = 200
            self._set_content(request_url)
        else:
            self.status_code = 500

    def _set_content(self, request_url: str) -> None:
        '''Set mocked response content based on request url'''

        content = {}

        if SWAPI_RESOURCE_REGEX.match(request_url):

            content = {resource: 'is what you asked for'}

        elif SWAPI_RESOURCE_SCHEMA_REGEX.match(request_url):
            resource = (expected_url_format.match(url)).group(1)
            content = {resource: 'is the schema you asked for'}

        elif SWAPI_BASE_REGEX.match(request_url):
            for resource in SWAPI_RESOURCES:
                content[resource] = None
        else:
            return None

        self.content = (json.dumps(content)).encode('utf-8')


@pytest.fixture()
def mock_swapi_connection(monkeypatch):
    def generate_mock_swapi_response(request_url):
        return MockSwapiResponse(request_url)

    monkeypatch.setattr(requests, 'get', generate_mock_swapi_response)
