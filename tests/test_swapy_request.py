import pytest


from swapy import SwapyRequest

def test_object_creation():

    myswapy = SwapyRequest()

    content = myswapy.make_request('planets', 1, True)

    print('content')
    print(content)

    content = myswapy.get_resource_schema('planets')
    print('schema')
    print(content)

    assert 1 == 0