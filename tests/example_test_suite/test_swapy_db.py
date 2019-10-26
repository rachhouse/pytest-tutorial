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

    test_film = {
        "characters": [
            "https://swapi.co/api/people/1/",
            "https://swapi.co/api/people/1/",
        ],
        "created": "2014-12-10T14:23:31.880000Z",
        "director": "George Lucas",
        "edited": "2014-12-12T11:24:39.858000Z",
        "episode_id": 4,
        "opening_crawl": "It is a period of civil war.\n\nRebel spaceships, striking\n\nfrom a hidden base, have won\n\ntheir first victory against\n\nthe evil Galactic Empire.\n\n\n\nDuring the battle, Rebel\n\nspies managed to steal secret\r\nplans to the Empire's\n\nultimate weapon, the DEATH\n\nSTAR, an armored space\n\nstation with enough power\n\nto destroy an entire planet.\n\n\n\nPursued by the Empire's\n\nsinister agents, Princess\n\nLeia races home aboard her\n\nstarship, custodian of the\n\nstolen plans that can save her\n\npeople and restore\n\nfreedom to the galaxy....",
        "planets": ["https://swapi.co/api/planets/1/"],
        "producer": "Gary Kurtz, Rick McCallum",
        "release_date": "1977-05-25",
        "species": [
            "https://swapi.co/api/species/1/",
            "https://swapi.co/api/species/2/",
        ],
        "starships": [
            "https://swapi.co/api/starships/2/",
            "https://swapi.co/api/starships/3/",
        ],
        "title": "A New Hope",
        "url": "https://swapi.co/api/films/1/",
        "vehicles": [
            "https://swapi.co/api/vehicles/4/",
            "https://swapi.co/api/vehicles/5/",
        ],
    }

    swapydb._insert_resource(test_film, 'films', 1)

    assert 1 == 0
