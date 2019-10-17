import pytest

from swapy import Swapy, SwapyException


def test_object_init():
    '''Test Swapy object creates with default arguments (none)'''

    swapy = Swapy()

    assert swapy._wookiee == False, 'default wookiee setting should be false'


def test_get_all_available_resources(mock_swapi_connection):
    swapy = Swapy()

    assert swapy._swapi_resource_list == None

    all_expected_resources = [
        'films',
        'people',
        'planets',
        'species',
        'starships',
        'vehicles',
    ]

    assert swapy.get_all_available_resources() == all_expected_resources
    assert swapy._swapi_resource_list == all_expected_resources


def test_validate_resource():
    '''Test validate_resource correctly identifies valid and invalid swapi resources'''

    swapy = Swapy()

    for valid_resource in ['films', 'people']:
        assert swapy._validate_resource(valid_resource) == None

    for invalid_resource in ['babbityrabbity', 'planet']:
        with pytest.raises(SwapyException):
            swapy._validate_resource(invalid_resource) == None
