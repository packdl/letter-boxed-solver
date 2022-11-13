import pprint as pp
from collections import defaultdict
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
        if a in side:
            return side


def get_unused_letters(my_word, g_letters):
    my_word = set(my_word)
    g_letters = set(g_letters)
    return g_letters.difference(my_word)


def check_for_unused_letters(word, unused_letters):
    return any(letter in unused_letters for letter in word)


with open("/usr/share/dict/words", "r") as dictionary, open("all_words", "w") as output:
    for word in dictionary:
        word = word.strip()
        if (
            word[0].islower()
            and len(word) >= 4
            and all(letter in game_letters for letter in word.lower())  # type: ignore
        ):
            output.write(word + "\n")

with open("all_words", "r") as reduced_list, open("valid_words", "w") as valid_file:
    for word in reduced_list:
        word = word.lower().strip()
        if not word:
            break

        valid_word = True
        for a, b in zip(word, word[1:]):
            if a == b:
                valid_word = False
                break
            side = get_side(a, [side1, side2, side3, side4])
            # print(a, side, word)
            if side:
                if b in side:
                    valid_word = False
                    break
        if valid_word:
            valid_file.write(word + "\n")

num_let_dict = defaultdict(list)
words = []
with open("valid_words", "r") as valid_file:
    for word in valid_file:
        word = word.strip()
        if word:
            num_let_dict[(len(word), word[0])].append(word)
            words.append(word)

sorted_keys = sorted(num_let_dict, reverse=True)

answers = []
for word in words:
    letters_left = get_unused_letters(word, game_letters)
    potential_answer = []
    potential_answer.append(word)
    for x in range(1, max_size):
        filter_keys = (key for key in sorted_keys if key[1] == word[-1])
        key = choice(list(filter_keys))
        word = choice(num_let_dict[key])
        potential_answer.append(word)
        if not get_unused_letters("".join(potential_answer), game_letters):
            answers.append(potential_answer)
            break
answers.sort(key=lambda x: len(x))
pp.pprint(answers)
