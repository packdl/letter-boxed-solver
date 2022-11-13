import pprint as pp
from collections import defaultdict
from collections.abc import Iterator
from random import choice

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


def get_side(letter, sides):
    for side in sides:
        if letter in side:
            return side
    return []


def get_unused_letters(my_word, g_letters):
    my_word = set(my_word)
    g_letters = set(g_letters)
    return g_letters.difference(my_word)


def check_for_unused_letters(word, unused_letters):
    return any(letter in unused_letters for letter in word)


def generate_valid_words(dictionary_path: str = None) -> Iterator[str]:
    if not dictionary_path:
        dictionary_path = "/usr/share/dict/words"

        with open(dictionary_path, "r") as dictionary:
            for word in dictionary:
                word = word.strip()
                if (
                    word[0].islower()
                    and len(word) >= 3
                    and all(letter in game_letters for letter in word.lower())  # type: ignore
                ):
                    word = word.lower().strip()
                    if not word:
                        continue

                    valid_word = is_word_valid(word)
                    if valid_word:
                        yield word
                else:
                    continue


def is_word_valid(word):
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


words = list(generate_valid_words())


def get_ranked_words(words) -> dict:
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


num_let_dict = get_ranked_words(words)

sorted_keys = sorted(num_let_dict, reverse=True)

answers = []
used = set()


def dfs(word: str, possible_answer: tuple):

    if len(possible_answer) >= max_size or word in used:
        return

    possible_answer = possible_answer + (word,)
    letters_left = get_unused_letters("".join(possible_answer), game_letters)
    if letters_left:

        filter_keys = (key for key in sorted_keys if key[1] == word[-1])
        for key in sorted(filter_keys, reverse=True):
            for next_word in num_let_dict[key]:
                dfs(next_word, possible_answer)
    else:
        used.update(possible_answer)
        answers.append(possible_answer)
        return


if __name__ == "__main__":
    for key in sorted_keys:
        for word in num_let_dict[key]:
            dfs(word, tuple())
    pp.pprint(answers)
