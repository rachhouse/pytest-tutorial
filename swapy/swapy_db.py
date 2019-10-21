import os
import pathlib
import sqlite3

from typing import Dict


class SwapyDB:
    def __init__(self) -> None:
        self._setup_dirs()

        self._conn = sqlite3.connect(self._db_path)
        self._cursor = self._conn.cursor()

    def _get_base_dir(self) -> pathlib.Path:
        '''Return parent directory of current file (ie. swapy code)'''
        return pathlib.Path(__file__).parent

    def _setup_dirs(self) -> None:
        '''Create .swapy_cache dir if it doesn't exist'''

        self._swapy_cache_dir = self._get_base_dir() / '.swapy_cache'

        if not os.path.exists(self._swapy_cache_dir):
            os.makedirs(self._swapy_cache_dir)

        self._db_path = self._swapy_cache_dir / 'swapy.sqlite'

    # def _create_sqlite_db(self):
    #     '''Create a swapy cache sqlite db if one doesn't exist'''

    def _parse_swapi_schema(self, schema: Dict):

        title = schema['required'].tolower()
        required_fields = schema['required']
        properties = schema['properties']


# nuke all tables and start over
# create a table based on swapi schema
# insert resource_id
# verify resource_id exists in table
