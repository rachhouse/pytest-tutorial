import json
import os
import pathlib
import pytest

from swapy import SwapyDB, SwapyException


@pytest.fixture()
def mock_swapy_cache_dir(monkeypatch, tmpdir):
    '''Mock swapy's base dir using tmpdir'''

    def return_mocked_base_dir(self):
        return pathlib.Path(tmpdir)

    monkeypatch.setattr(SwapyDB, '_get_base_dir', return_mocked_base_dir)


def test_object_init(mock_swapy_cache_dir, tmpdir, mock_swapi_connection):
    '''Test SwapyDB object creates with default arguments (none) 
    and creates .swapy_cache dir'''

    swapydb = SwapyDB()

    # check for creation of .swapy_cache and swapy.sqlite
    expected_swapy_cache_dir = pathlib.Path(tmpdir) / '.swapy_cache'
    expected_swapy_db_path = expected_swapy_cache_dir / 'swapy.sqlite'

    assert os.path.isdir(expected_swapy_cache_dir)
    assert os.path.exists(expected_swapy_db_path)


def test_decode_swapi_url_valid():
    '''Test that resource info can be extracted from valid swapi urls'''

    swapydb = SwapyDB()

    test_cases = {
        1: {
            'url': 'https://swapi.co/api/species/1/',
            'expected_resource': 'species',
            'expected_resource_id': 1,
        },
        2: {
            'url': 'https://swapi.co/api/planets/5',
            'expected_resource': 'planets',
            'expected_resource_id': 5,
        },
    }

    for id, test_case in test_cases.items():
        resource, resource_id = swapydb._decode_swapi_url(test_cases[id]['url'])
        assert resource == test_cases[id]['expected_resource']
        assert resource_id == test_cases[id]['expected_resource_id']


def test_decode_swapi_url_invalid():
    '''Test that decoding an invalid swapi url throws an error'''

    swapydb = SwapyDB()

    with pytest.raises(SwapyException) as swapy_exception:
        swapydb._decode_swapi_url('gobbldegook')

    assert str(swapy_exception.value) == 'bad swapi url format'


def test_stuff(expected_swapi_resources, datadir, mock_swapi_connection):

    swapydb = SwapyDB()

    swapydb._deathstar()

    # load sample schema
    for resource in list(expected_swapi_resources.keys()):
        resource_schema_file = pathlib.Path(
            datadir.join('swapi_{}_schema.json'.format(resource))
        )

        with open(resource_schema_file, 'r') as fh:
            resource_schema = json.loads(fh.read())

        swapydb._create_tables_for_resource(resource, resource_schema)

    test_thing_type = 'vehicles'
    test_thing = {
        'name': 'Sand Crawler',
        'model': 'Digger Crawler',
        'manufacturer': 'Corellia Mining Corporation',
        'cost_in_credits': '150000',
        'length': '36.8',
        'max_atmosphering_speed': '30',
        'crew': '46',
        'passengers': '30',
        'cargo_capacity': '50000',
        'consumables': '2 months',
        'vehicle_class': 'wheeled',
        'pilots': [],
        'films': ['https://swapi.co/api/films/5/', 'https://swapi.co/api/films/1/'],
        'created': '2014-12-10T15:36:25.724000Z',
        'edited': '2014-12-22T18:21:15.523587Z',
        'url': 'https://swapi.co/api/vehicles/4/',
    }

    swapydb._insert_resource(test_thing, test_thing_type, 1)

    assert 1 == 0
