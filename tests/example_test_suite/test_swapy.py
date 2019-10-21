import pytest

from swapy import Swapy, SwapyException


def test_object_init():
    '''Test Swapy object creates with default arguments (none)'''

    swapy = Swapy()
    assert swapy._wookiee == False, 'default wookiee setting should be false'


def test_get_all_available_resources(mock_swapi_connection, expected_swapi_resources):
    '''Test that get_all_available_resources call a) returns the correct resources
    and b) caches the results in the Swapy object'''

    swapy = Swapy()

    assert swapy._swapi_resource_list == None

    all_expected_resources = list(expected_swapi_resources.keys())
    all_expected_resources.sort()

    assert swapy.get_all_available_resources() == all_expected_resources
    assert swapy._swapi_resource_list == all_expected_resources


def test_validate_resource(mock_swapi_connection):
    '''Test validate_resource correctly identifies valid and invalid swapi resources'''

    swapy = Swapy()

    for valid_resource in ['films', 'people']:
        assert swapy._validate_resource(valid_resource) == None

    for invalid_resource in ['babbityrabbity', 'planet']:
        with pytest.raises(SwapyException) as swapy_exception:
            swapy._validate_resource(invalid_resource) == None

        assert str(swapy_exception.value) == 'bad swapi resource'
