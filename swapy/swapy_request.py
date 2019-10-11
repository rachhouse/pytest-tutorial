import json
import requests

BASE_URL = 'https://swapi.co/api'


class SwapyRequest:
    def make_request(self, resource, id, wookiee=False):

        url = '{}/{}/{}/'.format(BASE_URL, resource, id)

        if wookiee:
            url = url + '?format=wookiee'

        print(url)

        response = requests.get(url)

        if response.status_code != 200:
            raise Exception('swapi returned a non-200 HTTP status code')

        return self._process_response_content(response)

    def _process_response_content(self, response):
        content = json.loads(response.content.decode('utf-8'))
        return content


    def get_resource_schema(self, resource):
        url = '{}/{}/schema'.format(BASE_URL, resource)

        response = requests.get(url)

        if response.status_code != 200:
            raise Exception('swapi returned a non-200 HTTP status code')

        return self._process_response_content(response)        

    def _get_resource_and_id_from_url(self, swapi_url):
        pass