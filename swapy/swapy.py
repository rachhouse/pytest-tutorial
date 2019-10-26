from typing import Dict, List

from .swapy_base import SwapyException, SwapyBase


class Swapy(SwapyBase):
    def __init__(self, wookiee: bool = False) -> None:
        SwapyBase.__init__(self, wookiee)

        self._swapi_resource_list = None

    def get_all_resource_types(self) -> List:
        '''Return a list of all available swapi resources
        Cache results from api to avoid incessant repetition of this call'''

        if self._swapi_resource_list is None:
            all_resources_url = self._assemble_swapi_url()
            all_resources = self._make_request(all_resources_url)
            all_resources = list(all_resources.keys())
            all_resources.sort()

            self._swapi_resource_list = all_resources

        return self._swapi_resource_list

    def _validate_resource(self, resource: str) -> None:
        '''Throws exception if resource is not a valid swapi resource'''
        if resource not in self.get_all_resource_types():
            raise SwapyException('bad swapi resource')

    def get_resource_schema(self, resource_type: str) -> Dict:
        '''Return schema for swapi resource'''

        self._validate_resource(resource_type)

        resource_url = self._assemble_swapi_url(resource_type, schema=True)
        resource_schema = self._make_request(resource_url)

        return resource_schema

    def get_resource_id(self, resource_type: str, resource_id: int) -> Dict:
        '''Return specific swapi resource identified by resource_id'''

        self._validate_resource(resource_type)

        resource_url = self._assemble_swapi_url(resource_type, resource_id)
        resource = self._make_request(resource_url)

        return resource

    def get_all_resources_of_type(self, resource_type: str) -> List[Dict]:
        '''Return all swapi objects of requested resource type'''

        self._validate_resource(resource_type)

        all_resources, resource_count = [], 0
        next_page_url = self._assemble_swapi_url(resource_type)

        # when requesting multiple objects, results may be paged depending on count
        while next_page_url is not None:
            resources_response = self._make_request(next_page_url)

            all_resources.extend(resources_response['results'])
            resource_count += resources_response['count']
            next_page_url = resources_response['next']

        print(
            'Fetched {} {} resources from swapi.'.format(resource_count, resource_type)
        )

        return all_resources
