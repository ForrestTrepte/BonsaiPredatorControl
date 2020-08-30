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
LION_HUNT_RATE = 0.5 # number of gazelles killed per lion hunting
LION_FOOD_CONSUMATION = 0.1 # number of gazelles eaten per lion
MAXIMUM_LION_POPULATION = 10000
GAZELLE_NET_REPRODUCE_RATE = 0.10
MAXIMUM_GAZELLE_POPULATION = 10000

# Model parameters
class CartPoleModel():
    def __init__(self):
        self.reset()

    def reset(self,
             initial_lion_population: float = 0,
             initial_gazelle_population: float = 0
        ):
        # cart position (m)
        self._lion_population = initial_lion_population
        self._gazelle_population = initial_gazelle_population
        self._lion_food = self._lion_population * LION_FOOD_CONSUMATION # enough food for first step
        print(f'reset: lion_population {self._lion_population}, gazelle_population {self._gazelle_population}')

    def step(self, command: float):
        # 1 for reproduce
        # 2 for hunt
        # otherwise rest

        # TODO: Apply probabilities to reproduction, hunting, death, etc. instead of just multiplying and rounding.

        if command == 1:
            self._lion_population += math.floor(self._lion_population * LION_REPRODUCE_BIRTH_RATE)
        elif command == 2:
            kills = math.floor(min(self._lion_population * LION_HUNT_RATE, self._gazelle_population))
            self._lion_food += kills
            self._gazelle_population -= kills
        
        self._lion_population -= math.floor(self._lion_population * LION_DEATH_RATE)
        self._lion_population = math.floor(min(self._lion_population, self._lion_food / LION_FOOD_CONSUMATION))
        self._lion_food -= self._lion_population * LION_FOOD_CONSUMATION
        self._lion_population = min(self._lion_population, MAXIMUM_LION_POPULATION)

        self._gazelle_population += math.floor(self._gazelle_population * GAZELLE_NET_REPRODUCE_RATE)
        self._gazelle_population = min(self._gazelle_population, MAXIMUM_GAZELLE_POPULATION)
