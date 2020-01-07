# Pacman Multi-Agent Search

UC Berkeley CS 188 Multi-Agent Search Project:

Implementing minimax and expactimax search, and design of an evaluation function.

## Installation

Built in python version 3.6

Can install using [pipenv](https://pipenv-fork.readthedocs.io/en/latest/).

## Reflex Agent

To visualize the reflex agent:

```bash
pacman.py --frameTime 0 -p ReflexAgent -k 2
```

To grade the reflex agent:

```bash
autograder.py -q q1 --no-graphics
```

## Minimax Algorithm

To visualize the minimax adversarial search:

```bash
pacman.py -p MinimaxAgent -l minimaxClassic -a depth=4
```

To grade the minimax adversarial search:

```bash
autograder.py -q q2 --no-graphics
```