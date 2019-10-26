import json
import requests

from typing import Dict, Optional

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
        self,
        resource: Optional[str] = None,
        resource_id: Optional[int] = None,
        schema: Optional[bool] = False,
    ) -> SwapiURL:
        '''Return URL for swapi api request based on optional resource/resource id/schema'''

        # default to returning swapi base url
        url = BASE_URL

        if schema == True:
            url = '{}/{}/schema'.format(BASE_URL, resource)
        elif (resource is not None) and (resource_id is not None):
            url = '{}/{}/{}/'.format(BASE_URL, resource, resource_id)
        elif (resource is not None) and (resource_id is None):
            url = '{}/{}/'.format(BASE_URL, resource)

        if self._wookiee:
            url = url + '?format=wookiee'

        return url


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
            print(response)
            raise SwapyException('swapi returned a non-200 HTTP status code: {}'.format(response.status_code))

        return response.content

    def _process_response_content(self, response_content: bytes) -> SwapiResponse:
        '''Decode swapi response_content JSON'''

        try:
            content = json.loads(response_content.decode('utf-8'))
        except:
            raise SwapyException('Could not parse swapi response content')

        return content
