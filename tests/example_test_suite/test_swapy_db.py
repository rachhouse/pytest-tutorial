import json
import os
import pathlib
import pytest

from swapy import Swapy, SwapyDB


@pytest.fixture()
def mock_swapy_cache_dir(monkeypatch, tmpdir):
    '''Mock swapy's base dir using tmpdir'''

    def return_mocked_base_dir(self):
        return pathlib.Path(tmpdir)

    monkeypatch.setattr(SwapyDB, '_get_base_dir', return_mocked_base_dir)


def test_object_init(mock_swapy_cache_dir, tmpdir):
    '''Test SwapyDB object creates with default arguments (none) 
    and creates .swapy_cache dir'''

    swapydb = SwapyDB()

    # check for creation of .swapy_cache and swapy.sqlite
    expected_swapy_cache_dir = pathlib.Path(tmpdir) / '.swapy_cache'
    expected_swapy_db_path = expected_swapy_cache_dir / 'swapy.sqlite'

    assert os.path.isdir(expected_swapy_cache_dir)
    assert os.path.exists(expected_swapy_db_path)


def test_stuff(expected_swapi_resources, datadir):

    swapydb = SwapyDB()

    # load sample schema
    planet_schema_file = pathlib.Path(datadir.join('swapi_planet_schema.json'))
    with open(schema_file, 'r') as fh:
        planet_schema = json.loads(fh.read())

    swapydb._parse_swapi_schema(planet_schema)

    assert 1 == 0
