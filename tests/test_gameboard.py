from lbsolver.lbsolver import Gameboard
from contextlib import nullcontext
import pytest


def test_valid_board():
    gb1 = Gameboard("n w r a b i c o d e l t".split())
    assert gb1.side1 == "nwr"

    gb1 = Gameboard("nwrabicodelt")
    assert gb1.side1 == "nwr"
    assert gb1.side2 == "abi"
    assert gb1.side3 == "cod"
    assert gb1.side4 == "elt"

    assert gb1.get_side_for_letter("n") == "nwr"
    assert gb1.get_side_for_letter("l") == "elt"
    assert gb1.get_side_for_letter("s") is None


@pytest.mark.parametrize(
    "my_input,expectation",
    [
        ("123k34dlkdfj", pytest.raises(ValueError)),
        ("abcdefg", pytest.raises(ValueError)),
        ("abcdefghijkl", nullcontext()),
        ("abcdefghijklm", pytest.raises(ValueError)),
        ("aaabbbcccddd", pytest.raises(ValueError)),
    ],
)
def test_valid_and_invalid_boards(my_input, expectation):
    with expectation:
        Gameboard(my_input)
