import pytest

from swapy import Swapy


def test_create_swapy_object():

    swapy = Swapy(use_cache=False)

    assert swapy._wookiee == False, 'default wookiee setting should be false'
