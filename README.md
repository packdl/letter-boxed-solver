# Introduction
This is a simple script to solve the [NYT Letter Boxed game](https://www.nytimes.com/puzzles/letter-boxed). The user supplies a words file and a Letter Boxed gamehe words file is used to generate winning combinations for Letter Boxed. 

Good recommendations for words files include:
- The [words](https://en.wikipedia.org/wiki/Words_(Unix)) file included with Linux
- The Moby II projects [common](https://www.gutenberg.org/files/3201/files/COMMON.TXT) words file

# Usage
## Using an example on a Python REPL in Linux
```
from lbsolver.lbsolver import Gameboard, LBSolver
board = Gameboard("t n m h r v i k e a u b".split())
FILE = '/usr/share/dict/words'
with open(FILE,'r') as my_file:
    dictionary = my_file.readlines()


solver = LBSolver(board, dictionary)
answers = solver.solve(max_num_words=3, minimum_answers=10)
print(answers)
```
## Command line
Type the following at the command prompt to see command line usage:
```
lbsolver -h
```
# Our License
[Our License](LICENSE)