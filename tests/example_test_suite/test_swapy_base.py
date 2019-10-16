import pytest

from swapy import SwapyBase, SwapyException

SWAPI_BASE_URL = 'https://swapi.co/api'


def test_assemble_swapi_url():
    '''Test that swapi api request urls are assembled correctly'''

    swapy_base = SwapyBase()

    # assemble base url
    assert swapy_base._assemble_swapi_url() == SWAPI_BASE_URL

    # assemble request for resource schema
    resource = 'planets'
    expected_url = 'https://swapi.co/api/planets/schema'
    assert swapy_base._assemble_swapi_url(resource) == expected_url

    # assemble request for individual resource
    resource, resource_id = 'species', 1
    expected_url = 'https://swapi.co/api/species/1/'
    assert swapy_base._assemble_swapi_url(resource, resource_id) == expected_url

    swapy_base_wookiee = SwapyBase(wookiee=True)

    # assemble request for individual resource in wookiee format
    resource, resource_id = 'species', 1
    expected_url = 'https://swapi.co/api/species/1/?format=wookiee'
    assert swapy_base_wookiee._assemble_swapi_url(resource, resource_id) == expected_url


def test_decode_swapi_url_valid():

    swapy_base = SwapyBase()

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
        resource, resource_id = swapy_base._decode_swapi_url(test_cases[id]['url'])
        assert resource == test_cases[id]['expected_resource']
        assert resource_id == test_cases[id]['expected_resource_id']


def test_decode_swapi_url_invalid():
    swapy_base = SwapyBase()

    with pytest.raises(SwapyException):
        swapy_base._decode_swapi_url('gobbldegook')
