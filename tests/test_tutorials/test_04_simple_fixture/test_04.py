import pytest

from swapy import SwapyBase


@pytest.fixture()
def swapi_base_url():
    return 'https://swapi.co/api'


def test_assemble_swapi_url(swapi_base_url):
    '''Test that swapi api request urls are assembled correctly'''

    swapy_base = SwapyBase()

    # no args to _assemble_swapi_url yields swapi base url
    assert swapy_base._assemble_swapi_url() == swapi_base_url

    # test return of swapi schema url
    resource = 'planets'
    expected_url = '{}/planets/schema'.format(swapi_base_url)
    assert swapy_base._assemble_swapi_url(resource, schema=True) == expected_url
