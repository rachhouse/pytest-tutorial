import pytest

from swapy import Swapy, SwapyException


def test_create_swapy_object_fails_with_bad_args():

    with pytest.raises(TypeError):
        swapy = Swapy(use_cache=False, my_crazy_arg='trekkies4eva')
