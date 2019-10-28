import pytest

from swapy import Swapy, SwapyException


@pytest.fixture()
def mock_swapydb(monkeypatch):
    '''Override init of new SwapyDB() in Swapy() class'''

    def return_none(self):
        return None

    monkeypatch.setattr(Swapy, '_get_swapy_db', return_none)
    monkeypatch.setattr(Swapy, '_setup_db_cache', return_none)


def test_object_init(mock_swapydb):
    '''Test Swapy object creates with default arguments (none)'''

    swapy = Swapy()
    assert swapy._wookiee == False, 'default wookiee setting should be false'


def test_get_all_resource_types(
    mock_swapi_connection, mock_swapydb, expected_swapi_resources
):
    '''Test that get_all_resource_types call a) returns the correct resources
    and b) caches the results in the Swapy object'''

    swapy = Swapy()

    assert swapy._swapi_resource_list == None

    all_expected_resources = list(expected_swapi_resources.keys())
    all_expected_resources.sort()

    assert swapy.get_all_resource_types() == all_expected_resources
    assert swapy._swapi_resource_list == all_expected_resources


def test_validate_resource(mock_swapi_connection, mock_swapydb):
    '''Test validate_resource correctly identifies valid and invalid swapi resources'''

    swapy = Swapy()

    for valid_resource in ['films', 'people']:
        assert swapy._validate_resource(valid_resource) == None

    for invalid_resource in ['babbityrabbity', 'planet']:
        with pytest.raises(SwapyException) as swapy_exception:
            swapy._validate_resource(invalid_resource) == None

        assert str(swapy_exception.value) == 'bad swapi resource'


@pytest.mark.live
def test_autopopulation_of_cached_schemas():
    '''Test that swapi schemas are autopopulated in the cache upon init'''

    swapy = Swapy()

    expected_schema_tables = [
        'films',
        'films2characters',
        'films2planets',
        'films2species',
        'films2starships',
        'films2vehicles',
        'people',
        'people2films',
        'people2species',
        'people2starships',
        'people2vehicles',
        'planets',
        'planets2films',
        'planets2residents',
        'species',
        'species2films',
        'species2people',
        'starships',
        'starships2films',
        'starships2pilots',
        'vehicles',
        'vehicles2films',
        'vehicles2pilots',
    ]

    newly_created_tables, _ = swapy._db.run_query(
        "select name from sqlite_master where type='table' order by name asc;"
    )
    newly_created_tables = [t[0] for t in newly_created_tables]

    assert newly_created_tables == expected_schema_tables
