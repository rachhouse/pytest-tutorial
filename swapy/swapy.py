import pathlib
import sqlite3

from typing import Dict, List

from .swapy_base import SwapyException, SwapyBase


class Swapy(SwapyBase):
    def __init__(self, wookiee: bool = False) -> None:
        SwapyBase.__init__(self, wookiee)

        self._swapi_resource_list = None

    def get_all_available_resources(self) -> List:
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
        if resource not in self.get_all_available_resources():
            raise SwapyException('bad resource')

    def get_resource_schema(self, resource: str) -> Dict:
        '''Return schema for swapi resource'''

        self._validate_resource(resource)

        resource_url = self._assemble_swapi_url(resource)
        resource_schema = self._make_request(resource_url)

        return resource_schema

    def get_resource_id(self, resource: str, resource_id: int) -> Dict:
        self._validate_resource(resource)

        resource_url = self._assemble_swapi_url(resource, resource_id)
        resource = self._make_request(resource_url)

        return resource
