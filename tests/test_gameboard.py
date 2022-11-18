from lbsolver.lbsolver import Gameboard
import pytest


def test_valid_board():
    gb1 = Gameboard("n w r a b i c o d e l t".split())
    assert gb1.side1 == "nwr"

    gb1 = Gameboard("nwrabicodelt")
    assert gb1.side1 == "nwr"
    assert gb1.side2 == "abi"
    assert gb1.side3 == "cod"
    assert gb1.side4 == "elt"


# @pytest.mark.parametrize("input,expectation",[])
def test_invalid_board():
    with pytest.raises(ValueError):
        gb1 = Gameboard("123k34dlkdfj")
