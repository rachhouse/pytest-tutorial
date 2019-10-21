import json
import re
import requests

from typing import Dict, Optional, Tuple

# custom types
SwapiURL = str
SwapiResponse = Dict

BASE_URL = 'https://swapi.co/api'


class SwapyException(Exception):
    '''Subclass Exception so that we can throw SwapyExceptions'''

    pass


class SwapyBase:
    '''Base class to interact with the Star Wars API (swapi)
    Serves as a wrapper for swapi requests/responses'''

    def __init__(self, wookiee: bool = False) -> None:
        self._wookiee = wookiee

    def _assemble_swapi_url(
        self, resource: Optional[str] = None, resource_id: Optional[int] = None
    ) -> SwapiURL:
        '''Return URL for swapi api request based on optional resource/resource id'''

        url = BASE_URL

        if (resource is not None) and (resource_id is not None):
            url = '{}/{}/{}/'.format(BASE_URL, resource, resource_id)
        elif (resource is not None) or (resource_id is not None):
            url = '{}/{}/schema'.format(BASE_URL, resource)

        if self._wookiee:
            url = url + '?format=wookiee'

        return url

    def _decode_swapi_url(self, url: SwapiURL) -> Tuple[str, int]:
        '''Extract resource and resource id from a swapi url'''

        expected_url_format = re.compile(re.escape(BASE_URL) + r"\/(\w+)\/(\d+)\/*")

        if not expected_url_format.match(url):
            raise SwapyException('bad swapi url format')

        match = expected_url_format.match(url)
        return match.group(1), int(match.group(2))

    def _make_request(self, request_url: SwapiURL) -> SwapiResponse:
        '''Query swapi with input request_url, format response content into dict'''

        print('Requesting {}'.format(request_url))
        response_content = self._get(request_url)
        swapi_content = self._process_response_content(response_content)

        return swapi_content

    def _get(self, request_url: SwapiURL) -> bytes:
        '''Send HTTP request to swapi for request_url, return response content'''

        response = requests.get(request_url)

        if response.status_code != 200:
            raise SwapyException('swapi returned a non-200 HTTP status code')

        return response.content

    def _process_response_content(self, response_content: bytes) -> SwapiResponse:
        '''Decode swapi response_content JSON'''

        try:
            content = json.loads(response_content.decode('utf-8'))
        except:
            raise SwapyException('Could not parse swapi response content')

        return content
