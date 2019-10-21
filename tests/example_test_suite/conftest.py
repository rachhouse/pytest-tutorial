import json
import os
import pytest
import re
import requests

from distutils import dir_util

BASE_URL = 'https://swapi.co/api'

SWAPI_RESOURCE_REGEX = re.compile(re.escape(BASE_URL) + r"\/(\w+)\/(\d+)\/*$")
SWAPI_RESOURCE_SCHEMA_REGEX = re.compile(re.escape(BASE_URL) + r"\/(\w+)\/*$")
SWAPI_BASE_REGEX = re.compile(re.escape(BASE_URL))

SWAPI_RESOURCES = ['films', 'people', 'planets', 'species', 'starships', 'vehicles']


@pytest.fixture()
def swapi_base_url():
    return BASE_URL


class MockSwapiResponse:
    '''Mocks a HTTP response object from swapi'''

    def __init__(self, request_url: str) -> None:
        if SWAPI_BASE_REGEX.match(request_url):
            self.status_code = 200
            self._set_content(request_url)
        elif re.compile(r"mock_bad_json").match(request_url):
            self.status_code = 200
            self.content = '{ this is gibberish }'
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
    '''Override requests.get to return mocked swapi content'''

    def generate_mock_swapi_response(request_url):
        return MockSwapiResponse(request_url)

    monkeypatch.setattr(requests, 'get', generate_mock_swapi_response)


@pytest.fixture()
def expected_swapi_resources():
    '''Generate list of expected swapi resources'''

    expected_swapi_resources = {}

    for resource_key in SWAPI_RESOURCES:
        expected_swapi_resources[resource_key] = '{}/{}/'.format(BASE_URL, resource_key)

    return expected_swapi_resources


@pytest.fixture()
def datadir(tmpdir, request):
    """Method to make test data files available to pytest at test runtime"""

    # get filename of current test file, and look for data directory of same name
    filename = request.module.__file__
    test_dir, _ = os.path.splitext(filename)

    # if the filename is a directory, copy all files in directory to tmpdir
    if os.path.isdir(test_dir):
        dir_util.copy_tree(test_dir, str(tmpdir))

    return tmpdir
