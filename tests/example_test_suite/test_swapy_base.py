import pytest

from swapy import SwapyBase, SwapyException


def test_object_init():
    '''Test SwapyBase object creates with default arguments (none)'''

    swapy_base = SwapyBase()
    assert swapy_base._wookiee == False, 'default wookiee setting should be false'


def test_assemble_swapi_url(swapi_base_url):
    '''Test that swapi api request urls are assembled correctly'''

    swapy_base = SwapyBase()

    # assemble base url
    assert swapy_base._assemble_swapi_url() == swapi_base_url

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
    '''Test that resource info can be extracted from valid swapi urls'''

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
    '''Test that decoding an invalid swapi url throws an error'''

    swapy_base = SwapyBase()

    with pytest.raises(SwapyException) as swapy_exception:
        swapy_base._decode_swapi_url('gobbldegook')

    assert str(swapy_exception.value) == 'bad swapi url format'


@pytest.mark.live
def test_make_request(swapi_base_url, expected_swapi_resources):
    '''Test live call to swapi'''

    swapy_base = SwapyBase()
    swapi_resources = swapy_base._make_request(swapi_base_url)
    assert swapi_resources == expected_swapi_resources


def test_make_request_errors(mock_swapi_connection):
    '''Test that swapi response problems raise exceptions'''

    swapy_base = SwapyBase()

    with pytest.raises(SwapyException) as swapy_exception:
        swapi_content = swapy_base._make_request('a terrible url')

    assert str(swapy_exception.value) == 'swapi returned a non-200 HTTP status code'

    with pytest.raises(SwapyException) as swapy_exception:
        swapi_content = swapy_base._make_request('mock_bad_json')

    assert str(swapy_exception.value) == 'Could not parse swapi response content'
