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


def test_decode_swapi_url_valid(mock_swapy_cache_dir):
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


def test_decode_swapi_url_invalid(mock_swapy_cache_dir):
    '''Test that decoding an invalid swapi url throws an error'''

    swapydb = SwapyDB()

    with pytest.raises(SwapyException) as swapy_exception:
        swapydb._decode_swapi_url('gobbldegook')

    assert str(swapy_exception.value) == 'bad swapi url format'


def test_schema_creation_and_resource_insertion(
    mock_swapy_cache_dir, expected_swapi_resources, datadir
):
    '''Test that schemas and resources are created/inserted correctly based on input schema json, 
    and we don't get any sqlite errors'''

    swapydb = SwapyDB()

    # load example schemas
    for resource_type in list(expected_swapi_resources.keys()):
        resource_schema_file = pathlib.Path(
            datadir.join('schemas/swapi_{}_schema.json'.format(resource_type))
        )

        with open(resource_schema_file, 'r') as fh:
            resource_schema = json.loads(fh.read())

        swapydb._create_tables_for_resource(resource_type, resource_schema)

    # insert example resources
    for resource_type in list(expected_swapi_resources.keys()):
        resource_file = pathlib.Path(
            datadir.join('resources/swapi_example_{}.json'.format(resource_type))
        )

        with open(resource_file, 'r') as fh:
            resource = json.loads(fh.read())

        _, resource_id = swapydb._decode_swapi_url(resource['url'])

        swapydb._insert_resource(resource, resource_type, resource_id)

    test_queries = {
        '1': {'query': 'select count(*) from films2characters;', 'expected_answer': 18},
        '2': {'query': 'select count(*) from species;', 'expected_answer': 1},
    }

    for test in test_queries.keys():
        query = test_queries[test]['query']
        expected_answer = test_queries[test]['expected_answer']

        query_answer, _ = swapydb.run_query(query)

        assert query_answer[0][0] == expected_answer
