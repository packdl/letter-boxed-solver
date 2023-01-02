from contextlib import nullcontext
from pathlib import Path

import pytest
from lbsolver import Gameboard, LBSolver


@pytest.fixture
def gameboard1():
    return Gameboard("giyercpolahx")


@pytest.fixture
def gameboard2():
    return Gameboard("s l g a t i p r y h f o".split())


@pytest.fixture
def gameboard3():
    return Gameboard("a b c d e f g h i j k l".split())


@pytest.fixture
def dictionary():
    FILE = "/usr/share/dict/words"
    if not Path(FILE).exists():
        FILE = Path(".") / "test_dictionary"

    with open(FILE, "r", encoding="utf-8") as dictionary_file:
        dictionary_words = dictionary_file.readlines()
    return dictionary_words


@pytest.fixture
def dictionary2():
    return ["adgjbehk", "kcfil"]


@pytest.fixture
def lbsolver1(gameboard2, dictionary):
    return LBSolver(gameboard2, dictionary)


def test_LBSolver(gameboard1, gameboard2, dictionary):
    with nullcontext():
        solver = LBSolver(gameboard1, dictionary)
        solver.gameboard = gameboard2
        for letter in "slgatipryhfo":
            assert letter in solver.gameboard.board

        dict2 = ["dictionary", "puppy", "fish"]
        solver.dictionary = dict2
        assert dict2 == solver.dictionary
        solver.dictionary = dictionary

    with pytest.raises(TypeError):
        solver.dictionary = None

    with pytest.raises(TypeError):
        solver.gameboard = None


@pytest.mark.parametrize(
    "inputs,expectations",
    [
        ((gameboard1, dictionary), nullcontext()),
        ((gameboard2, dictionary), nullcontext()),
        ((None, None), pytest.raises(TypeError)),
        ((None, dictionary), pytest.raises(TypeError)),
        ((gameboard2, None), pytest.raises(TypeError)),
    ],
)
def test_error_LBSolver(inputs, expectations):
    with expectations:
        LBSolver(inputs[0], inputs[1])


@pytest.mark.parametrize(
    "inputs,outputs",
    [
        ("physiologists", 3),
        ("safaris", 7),
        ("polygraphs", 12 - len(set("polygraphs"))),
        ("flashlights", 12 - len(set("flashlights"))),
        ("sporty", 12 - len(set("sporty"))),
    ],
)
def test_unused_letters(lbsolver1, inputs, outputs):
    result = lbsolver1.get_unused_letters(inputs)
    assert len(set(inputs)) + outputs == 12


def test_invalid_word_unused_letter(lbsolver1):
    with pytest.raises(ValueError):
        lbsolver1.get_unused_letters("polygraphsx")


@pytest.mark.parametrize(
    "inputs,outputs",
    [
        ("physiologists", True),
        ("safaris", True),
        ("slg", False),
        ("safarisx", False),
        ("xsafari", False),
        ("sssaaafff", False),
    ],
)
def test_possible_on_board(lbsolver1, inputs, outputs):
    assert lbsolver1.possible_on_board(inputs) == outputs


def test_generate_valid_words(lbsolver1):
    results = list(
        lbsolver1.generate_valid_words(
            ["physiologists", "safaris", "slg", "xsafari", "", " "]
        )
    )
    assert "slg" not in results
    assert "physiologists" in results
    assert "" not in results
    assert " " not in results


def test_solver(gameboard3, dictionary2, lbsolver1, gameboard1, dictionary):
    solver = LBSolver(gameboard3, dictionary2)
    result = solver.solve()
    assert len(result) == 1
    assert set(result[0]) == set(dictionary2)

    assert len(lbsolver1.solve()) >= 1

    solver2 = LBSolver(gameboard1, dictionary)
    answer = solver2.solve(1)
    assert len(answer) == 1

    solver2 = LBSolver(gameboard1, dictionary)
    answer2 = solver2.solve(1, 1, skip="lexicography")
    assert len(answer2) == 0

    with pytest.raises(ValueError):
        solver2.solve(-1)

    with pytest.raises(ValueError):
        solver2.solve(3, -1)


def test_nonrepeating_answers(dictionary):
    solver = LBSolver(Gameboard.default_board(), dictionary)
    answers = solver.solve(8, 5)
    for answer in answers:
        assert len(answer) == len(set(answer))
