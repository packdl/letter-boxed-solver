import pprint as pp
from collections import defaultdict, namedtuple
from collections.abc import Iterator, Sequence
from random import choice
from typing import NamedTuple, Tuple, List
from dataclasses import dataclass


class Gameboard:
    def __init__(self, board: str | List[str]) -> None:
        """An board represented as a string.

        board - a str or a list of one character strings
        """

        if len(board) != 12:
            raise ValueError(f"{board} is not valid. Board must only be 12 characters")
        if isinstance(board, str):
            if not board.isalpha() or len(set(board)) != 12:
                raise ValueError(
                    f"{board} is not valid. Board must be alphabetic characters only and 12 unique characters"
                )
        else:
            if "".join(board).isalpha():
                raise ValueError(
                    f"{board} is not valid. Board must be alphabetic characters only"
                )
        self._board = "".join(board)

    @property
    def side1(self):
        return self._board[0:3]

    @property
    def side2(self):
        return self._board[3:6]

    @property
    def side3(self):
        return self._board[6:9]

    @property
    def side4(self):
        return self._board[9:12]

    @property
    def board(self):
        return list(self._board)

    def __repr__(self) -> str:
        return f"""Board: {self.board} 
        Side 1: {self.side1}
        Side 2: {self.side2}
        Side 3: {self.side3}
        Side 4: {self.side4}"""


try:
    with open("settings", "r") as settings:
        all_sides = settings.readline().strip().split(" ")
except:
    print("No settings file found. Using default test string.")
    all_sides = "4 n w r a b i c o d e l t".strip().split("")
try:
    max_size = int(all_sides[0])
except ValueError as e:
    max_size = 4

side1 = all_sides[1:4]
side2 = all_sides[4:7]
side3 = all_sides[7:10]
side4 = all_sides[10:13]
game_letters = side1 + side2 + side3 + side4


def get_side(letter, sides) -> list:
    for side in sides:
        if letter in side:
            return side
    return []


def get_unused_letters(my_word, g_letters) -> set:
    my_word = set(my_word)
    g_letters = set(g_letters)
    return g_letters.difference(my_word)


def check_for_unused_letters(word, unused_letters) -> bool:
    return any(letter in unused_letters for letter in word)


def generate_valid_words_from_file(file=None) -> Sequence[str]:
    if not file:
        file = "/usr/share/dict/words"

    with open(file, "r") as dictionary:
        dictionary_words = dictionary.readlines()
        return generate_valid_words(dictionary_words)


def generate_valid_words(dictionary: Sequence[str]) -> Sequence[str]:
    """Generate an iterable of valid words from a dictionary"""
    for item in dictionary:
        item = item.strip()
        if (
            item[0].islower()
            and len(item) >= 3
            and all(letter in game_letters for letter in item.lower())  # type: ignore
        ):
            item = item.lower().strip()
            if not item:
                continue

            valid_word = is_word_valid(item)
            if valid_word:
                yield item
        else:
            continue


def is_word_valid(word) -> bool:
    """Check whether a word is valid based upon Letter Boxed Game rules"""
    valid_word = True
    for a, b in zip(word, word[1:]):
        if a == b:
            valid_word = False
            break
        side = get_side(a, [side1, side2, side3, side4])
        if b in side:
            valid_word = False
            break
    return valid_word


valid_words = set(generate_valid_words_from_file())


def get_ranked_words(words=valid_words) -> dict[int, str]:
    """Organized valid words into a dictionary with a tuple as a key

    Key is a tuple(len(set(used letters)), first_letter_of_word) - A higher # of used letters is better ranked.
    Value is a list of words that start with the leter identified int they key
    """
    num_let_dict = defaultdict(list)
    for word in words:
        num_letters_used = len(game_letters) - len(
            get_unused_letters(word, game_letters)
        )
        num_let_dict[(num_letters_used, word[0])].append(word)
    return num_let_dict


ranked_words_dict = get_ranked_words()

sorted_keys = sorted(ranked_words_dict, reverse=True)

answers = []
used = set()


def dfs(word: str, possible_answer: tuple):

    if len(possible_answer) >= max_size or word in used or word not in valid_words:
        return

    possible_answer = possible_answer + (word,)
    letters_left = get_unused_letters("".join(possible_answer), game_letters)
    if letters_left:

        filter_keys = (key for key in sorted_keys if key[1] == word[-1])
        for key in sorted(filter_keys, reverse=True):
            for next_word in ranked_words_dict[key]:
                dfs(next_word, possible_answer)
    else:
        used.update(possible_answer)
        answers.append(possible_answer)
        return


if __name__ == "__main__":
    for key in sorted_keys:
        for word in ranked_words_dict[key]:
            dfs(word, tuple())
    pp.pprint(answers)
