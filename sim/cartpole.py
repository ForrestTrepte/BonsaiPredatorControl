"""
Classic cart-pole system implemented by Rich Sutton et al.
Derived from http://incompleteideas.net/sutton/book/code/pole.c
permalink: https://perma.cc/C9ZM-652R
"""
__copyright__ = "Copyright 2020, Microsoft Corp."

# pyright: strict

import math
import random

# Constants
LION_REPRODUCE_BIRTH_RATE = 0.25
LION_DEATH_RATE = 0.1
MAXIMUM_POPULATION = 10000

# Model parameters
class CartPoleModel():
    def __init__(self):
        self.reset()

    def reset(self,
             initial_lion_population: float = 0,
        ):
        # cart position (m)
        self._lion_population = initial_lion_population
        print(f'reset: lion_population {self._lion_population}')

    def step(self, command: float):
        # 1 for reproduce
        # otherwise rest

        if command == 1:
            self._lion_population += self._lion_population * LION_REPRODUCE_BIRTH_RATE
        
        self._lion_population -= self._lion_population * LION_DEATH_RATE
        self._lion_population = min(self._lion_population, MAXIMUM_POPULATION)