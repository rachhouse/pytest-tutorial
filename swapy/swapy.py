from typing import Dict, List

from .swapy_base import SwapyBase, SwapyException
from .swapy_db import SwapyDB


class Swapy(SwapyBase):
    def __init__(self, use_cache=True, wookiee: bool = False) -> None:
        SwapyBase.__init__(self, wookiee)

        self._swapi_resource_list = None
        self._use_cache = use_cache

        if self._use_cache:
            self._db = self._get_swapy_db()
            self._setup_db_cache()

    def _get_swapy_db(self):
        return SwapyDB()

    def _setup_db_cache(self) -> None:
        '''Check for existing schema tables in cache - if not present, create them'''

        # check if we already have tables created in cache
        existing_tables, _ = self._db.run_query(
            "select name from sqlite_master where type='table';"
        )

        if not existing_tables:
            resource_types = self.get_all_resource_types()

            for resource_type in resource_types:
                print('Creating cache table for {}'.format(resource_type))
                schema = self.get_resource_schema(resource_type)
                self._db._create_tables_for_resource(resource_type, schema)

    def get_all_resource_types(self) -> List:
        '''Return a list of all available swapi resources
        Cache results from api in object to avoid incessant repetition of this call'''

        if self._swapi_resource_list is None:
            all_resources_types_url = self._assemble_swapi_url()
            all_resource_types = self._make_request(all_resources_types_url)
            all_resource_types = list(all_resource_types.keys())
            all_resource_types.sort()

            self._swapi_resource_list = all_resource_types

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

        # check if we've cached this resource already
        resource_query = 'select * from {} where id = {};'.format(
            resource_type, resource_id
        )
        cached_resource, headers = self._db.run_query(resource_query)

        if not cached_resource:
            resource_url = self._assemble_swapi_url(resource_type, resource_id)
            resource = self._make_request(resource_url)
            self._db._insert_resource(resource, resource_type, resource_id)
            cached_resource, headers = self._db.run_query(resource_query)

        return dict(zip(headers, cached_resource[0]))

    def get_all_cached_resources_of_type(self, resource_type: str) -> List[Dict]:
        '''Return all cached swapi resources of type resource_type from the db'''

        self._validate_resource(resource_type)

        all_cached_resource_query = 'select * from {};'.format(resource_type)
        resources, headers = self._db.run_query(all_cached_resource_query)

        return [dict(zip(headers, resource)) for resource in resources]

    def get_all_cached_relationships(self, map_from: str, map_to) -> List[Dict]:
        '''Return all cached swapi resources of type resource_type from the db'''

        lookup_table_name = '{}2{}'.format(map_from, map_to)

        all_cached_resource_query = 'select * from {};'.format(lookup_table_name)
        resources, headers = self._db.run_query(all_cached_resource_query)

        return [dict(zip(headers, resource)) for resource in resources]

    def download_swapi_universe(self):
        '''Downloads all swapi data to swapy cache'''

        print('Downloading the swapi universe...')

        for resource_type in ['planets']:
            resources = self._download_all_resources_of_type(resource_type)

            for resource in resources:
                self._db._insert_resource(resource, resource_type)

        print('Finished universe download.')

    def _download_all_resources_of_type(self, resource_type: str) -> List[Dict]:
        '''Return all swapi objects of requested resource type'''

        self._validate_resource(resource_type)

        all_resources, resource_count = [], 0
        next_page_url = self._assemble_swapi_url(resource_type)

        # when requesting multiple objects, results may be paged depending on count
        while next_page_url is not None:
            resources_response = self._make_request(next_page_url)
            all_resources.extend(resources_response['results'])
            resource_count = resources_response['count']
            next_page_url = resources_response['next']

        print(
            'Fetched {} {} resources from swapi.'.format(resource_count, resource_type)
        )

        return all_resources
