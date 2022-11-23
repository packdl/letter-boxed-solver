from contextlib import nullcontext
import pytest
from lbsolver.lbsolver import Gameboard


def test_default_board():
    assert isinstance(Gameboard.default_board(), Gameboard)
    Gameboard.default_board().board == "g i y e r c p o l a h x".split()


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
    assert gb1.board == list("nwrabicodelt")
    assert "Side 1" in str(gb1) and "nwr" in str(gb1)


@pytest.mark.parametrize(
    "my_input,expectation",
    [
        ("123k34dlkdfj", pytest.raises(ValueError)),
        ("abcdefg", pytest.raises(ValueError)),
        ("abcdefghijkl", nullcontext()),
        (list("abcdefghijkl"), nullcontext()),
        ("abcdefghijklm", pytest.raises(ValueError)),
        ("aaabbbcccddd", pytest.raises(ValueError)),
        (["a", 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], pytest.raises(ValueError)),
        (
            ["a", "1", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k"],
            pytest.raises(ValueError),
        ),
    ],
)
def test_valid_and_invalid_boards(my_input, expectation):
    with expectation:
        Gameboard(my_input)
