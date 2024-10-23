# Presentation

Implementation of scrabble in python.

## TODO

- computer player finding best word by trying all possible combinations
- https://medium.com/@aydinschwa/coding-the-worlds-fastest-scrabble-program-in-python-2aa09db670e3r
- IA for computer player (reinforcement learning, neural network, Monte Carlo Tree Search, ...)


## Bugs

- Le wordPlacerChecker ne verifie pas si on peut suivre un mot, par exemple ajouter un "ez" à la fin d'un mot à l'infinitif il renverra True meme si le mot n'existe pas (avec seed 42, rajoute aurez à la fin de melia)


