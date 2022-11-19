from collections import defaultdict
from collections.abc import Iterator, Sequence
from typing import List
from pprint import pprint as pp


class Gameboard:
    """This is a class that represents a Gameboard for a solver. Takes a string
    representing the board.

    :param board: A string or list of strings that represent the board.
    :type board: list|str
    :raise ValueError: If the board is invalid (incorrect length, non-alphabet characters or repeated characters)
    """

    def __init__(self, board: str | List[str]) -> None:
        """This is the initialzer method."""

        if len(board) != 12:
            raise ValueError(f"{board} is not valid. Board must only be 12 characters")
        if isinstance(board, str):
            if not board.isalpha() or len(set(board)) != 12:
                raise ValueError(
                    f"{board} is not valid. Board must be alphabetic characters only and 12 unique characters"
                )
        else:
            if not "".join(board).isalpha():
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

    def get_side_for_letter(self, letter: str) -> str | None:
        sides = [self.side1, self.side2, self.side3, self.side4]

        for side in sides:
            if letter in side:
                return side
        return None


class LBSolver:
    """This is the solver class. It requires a :class:`lbsolver.lbsolver.Gameboard`
    and a dictionary to generate a set of answers to the Letter Boxed game.

        :param gameboard: A gameboard representing the letters in the Letter Boxed game
        :type gameboard: :class: `lbsolver.lbsolver.Gameboard`
        :param dictionary: A backing dictionary to use to find potential answers
        :type dictionary: Sequence

    """

    def __init__(self, gameboard: Gameboard, dictionary: Sequence[str]) -> None:
        """Constructor method"""
        self.__gameboard = gameboard
        self.__dictionary = dictionary
        self.__answers: List[tuple] = []

    @property
    def gameboard(self):
        return self.__gameboard

    @property
    def dictionary(self):
        return self.__dictionary

    def get_unused_letters(self, my_word: str) -> set:
        my_word_set = set(my_word)
        g_letters = set(list(self.gameboard.board))
        return g_letters.difference(my_word_set)

    def possible_on_board(self, word_sequence: str) -> bool:
        """Check whether a sequence is possible based upon Letter Box rules. It
        does not determine whether the sequence is a word.
        """
        valid_sequence = True
        a, b = ("", "")
        for a, b in zip(word_sequence, word_sequence[1:]):
            if a == b:
                valid_sequence = False
                break
            side = self.gameboard.get_side_for_letter(a)
            # side = get_side(a, [side1, side2, side3, side4])
            if not side:
                valid_sequence = False
                break
            elif b in side:
                valid_sequence = False
                break

        if not self.gameboard.get_side_for_letter(b):
            return False
        return valid_sequence

    def generate_valid_words(
        self, dictionary: Sequence[str] | None = None
    ) -> Iterator[str]:
        """Based on the current gameboard, generate a set of valid words from
        dictionary. If dictionary parameter is not set, default dictionary is used.
        """
        if not dictionary:
            dictionary = self.dictionary

        for item in dictionary:
            item = item.strip()
            if (
                item[0].islower()
                and len(item) >= 3
                and all(letter in self.gameboard.board for letter in item.lower())  # type: ignore
            ):
                item = item.lower().strip()
                if not item:
                    continue

                valid_word = self.possible_on_board(item)
                if valid_word:
                    yield item
            else:
                continue

    def solve(
        self, max_num_words: int = 3, minimum_answers: int = 1
    ) -> Sequence[tuple]:
        self.__answers.clear()

        word_ranking_map = defaultdict(list)
        valid_words = set(self.generate_valid_words())
        for word in valid_words:
            num_letters_used = len(self.gameboard.board) - len(
                self.get_unused_letters(word)
            )
            word_ranking_map[(num_letters_used, word[0])].append(word)
        sorted_keys = sorted(word_ranking_map, reverse=True)
        used = set()

        def dfs(word: str, possible_answer: tuple):
            if len(self.__answers) >= minimum_answers:
                return

            if (
                len(possible_answer) >= max_num_words
                or word in used
                or word not in valid_words
            ):
                return
            possible_answer = possible_answer + (word,)
            letters_left = self.get_unused_letters("".join(possible_answer))
            if letters_left:

                filter_keys = (key for key in sorted_keys if key[1] == word[-1])
                for key in sorted(filter_keys, reverse=True):
                    for next_word in word_ranking_map[key]:
                        dfs(next_word, possible_answer)
            else:
                used.update(possible_answer)
                self.__answers.append(possible_answer)
                return

        for key in sorted_keys:
            if len(self.__answers) >= minimum_answers:
                break
            for word in word_ranking_map[key]:
                dfs(word, tuple())
        return self.__answers


if __name__ == "__main__":

    myboard = Gameboard("g i y e r c p o l a h x".strip().split())

    file = "/usr/share/dict/words"

    with open(file, "r") as dictionary_file:
        dictionary_words = dictionary_file.readlines()

    solver = LBSolver(myboard, dictionary_words)
    pp(solver.solve(max_num_words=3, minimum_answers=10))

    # add a decline feature to intensionally skip words
    # Make it so we can reset to gameboard and dictionary used with solver
