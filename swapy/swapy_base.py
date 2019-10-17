import json
import re
import requests

from typing import Dict, Optional, Tuple

SwapiURLType = str
SwapiJSON = Dict

BASE_URL = 'https://swapi.co/api'


class SwapyException(Exception):
    pass


class SwapyBase:
    '''Base class to interact with the Star Wars API (swapi)
    Serves as a wrapper for swapi requests/responses'''

    def __init__(self, wookiee: bool = False) -> None:
        self._wookiee = wookiee

    def _assemble_swapi_url(
        self, resource: Optional[str] = None, resource_id: Optional[int] = None
    ) -> SwapiURLType:
        '''Return URL for swapi api request based on optional resource/resource id'''

        url = BASE_URL

        if (resource is not None) and (resource_id is not None):
            url = '{}/{}/{}/'.format(BASE_URL, resource, resource_id)
        elif (resource is not None) or (resource_id is not None):
            url = '{}/{}/schema'.format(BASE_URL, resource)

        if self._wookiee:
            url = url + '?format=wookiee'

        return url

    def _decode_swapi_url(self, url: SwapiURLType) -> Tuple[str, int]:
        '''Extract resource and resource id from a swapi url'''

        expected_url_format = re.compile(re.escape(BASE_URL) + r"\/(\w+)\/(\d+)\/*")

        if not expected_url_format.match(url):
            raise SwapyException('bad swapi url format')

        match = expected_url_format.match(url)
        return match.group(1), int(match.group(2))

    def _make_request(self, request_url: SwapiURLType) -> SwapiJSON:

        print('Requesting {}'.format(request_url))
        response = requests.get(request_url)

        if response.status_code != 200:
            raise SwapyException('swapi returned a non-200 HTTP status code')

        return self._process_response_content(response)

    def _process_response_content(self, response) -> SwapiJSON:
        content = json.loads(response.content.decode('utf-8'))
        return content
