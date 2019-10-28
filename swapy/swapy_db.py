import os
import pathlib
import re
import sqlite3

from typing import Dict, Optional, Tuple

from .swapy_base import SwapyException

SwapiURL = str

BASE_URL = 'https://swapi.co/api'


PEOPLE_COLUMN_ALIASES = ['characters', 'residents', 'pilots']


class SwapyDB:
    def __init__(self) -> None:
        self._setup_dirs()
        self._create_db_cursor()

    def _get_base_dir(self) -> pathlib.Path:
        '''Return parent directory of current file (ie. swapy code)'''
        return pathlib.Path(__file__).parent.parent

    def _setup_dirs(self) -> None:
        '''Create .swapy_cache dir if it doesn't exist'''

        self._swapy_cache_dir = self._get_base_dir() / '.swapy_cache'

        if not os.path.exists(self._swapy_cache_dir):
            os.makedirs(self._swapy_cache_dir)

        self._db_path = self._swapy_cache_dir / 'swapy.sqlite'

    def _create_db_cursor(self) -> None:
        self._conn = sqlite3.connect(self._db_path)
        self._cursor = self._conn.cursor()

    def _deathstar(self):
        '''Blow away and recreate swapy cache sqlite db'''
        print('Destroying swapy cache sqlite db')
        if os.path.exists(self._db_path):
            os.remove(self._db_path)
            self._create_db_cursor()

    def _create_tables_for_resource(self, resource_type: str, schema: Dict) -> None:
        create_table_statement, lookups = self._parse_swapi_schema(
            resource_type, schema
        )

        # print('Creating table {}'.format(resource_type))
        self._cursor.executescript(create_table_statement)

        # create lookup tables
        for lookup in lookups:
            # print('Creating lookup table {}'.format(lookup))
            self._create_lookup_table(lookup[0], lookup[1])

    def _create_lookup_table(self, resource_type1: str, resource_type2) -> None:

        table_name = '{}2{}'.format(resource_type1, resource_type2)

        create_table_statement = '''
        create table if not exists {table_name} (
          {col1} integer, 
          {col2} integer,
        primary key ({col1}, {col2})
        );
        '''.format(
            table_name=table_name, col1=resource_type1, col2=resource_type2
        )

        self._cursor.executescript(create_table_statement)

    def _parse_swapi_schema(self, resource_type: str, schema: Dict):

        # title field on swapi schemas is often incorrect,
        # use resource_type instead
        title = resource_type

        required_fields = schema['required']
        properties = schema['properties']
        lookups = []

        table_columns = [('id', 'int primary key')]

        for field in required_fields:
            field_type = properties[field]['type']

            if field_type == 'string':
                table_columns.append((field, 'text'))
            if field_type == 'array':
                # table_columns.append((field, 'integer'))
                lookups.append((title, field))

        table_columns = ','.join(['{} {}'.format(x[0], x[1]) for x in table_columns])

        create_table_statement = 'create table if not exists {} ({});'.format(
            title, table_columns
        )

        return create_table_statement, lookups

    def _insert_resource(
        self, resource_object: Dict, resource_type: str, resource_id: Optional[int]
    ) -> None:
        '''Insert swapi resource data into swapy cache db,
        also insert relationship data in lookup tables'''

        if resource_id is None:
            _, resource_id = self._decode_swapi_url(resource_object['url'])

        # get column names
        self._cursor.execute('PRAGMA table_info({});'.format(resource_type))

        table_columns = self._cursor.fetchall()
        table_columns = [t[1] for t in table_columns]

        column_names, column_values = [], []

        for column in table_columns:
            column_names.append(column)

            if column == 'id':
                column_values.append(str(resource_id))
            else:
                column_values.append(resource_object[column])

        insert_statement = 'insert into {} ({}) values ({});'.format(
            resource_type,
            ','.join(column_names),
            ','.join('"{}"'.format(v) for v in column_values),
        )

        self._cursor.execute(insert_statement)

        # get lookup tables
        self._cursor.execute(
            "select name from sqlite_master where type='table' and name like '{}2%';".format(
                resource_type
            )
        )
        lookup_tables = self._cursor.fetchall()
        lookup_tables = [t[0] for t in lookup_tables]

        for lookup in lookup_tables:
            map_from, map_to = lookup.split('2')
            map_to_urls = resource_object[map_to]
            map_to_ids = [self._decode_swapi_url(u)[1] for u in map_to_urls]

            # make sure we have a list of unique ids
            map_to_ids = list(set(map_to_ids))

            for map_to_id in map_to_ids:
                lookup_insert = 'insert into {} ({}, {}) values ({}, {});'.format(
                    lookup, map_from, map_to, resource_id, map_to_id
                )
                self._cursor.execute(lookup_insert)

        self._conn.commit()

    def _decode_swapi_url(self, url: SwapiURL) -> Tuple[str, int]:
        '''Extract resource and resource id from a swapi url'''

        expected_url_format = re.compile(re.escape(BASE_URL) + r"\/(\w+)\/(\d+)\/*")

        if not expected_url_format.match(url):
            raise SwapyException('bad swapi url format')

        match = expected_url_format.match(url)
        return match.group(1), int(match.group(2))

    # need a query method
    # insert automatically into the db when you grab a resource
    # always check cache first
    # initial setup of cache should hit swapi for schemas

    # add a method to download all swapi data to cache
