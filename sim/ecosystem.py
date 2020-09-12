# pyright: strict

import math
import random
import enum

class EcosystemConfiguration():
    LION_REPRODUCE_BIRTH_RATE: float = 0.25
    LION_DEATH_RATE: float = 0.1
    LION_HUNT_RATE: float = 0.5 # number of gazelles killed per lion hunting
    LION_FOOD_CONSUMPTION: float = 0.1 # number of gazelles eaten per lion
    MAXIMUM_LION_POPULATION: float = 10000
    GAZELLE_NET_REPRODUCE_RATE: float = 0.1
    MAXIMUM_GAZELLE_POPULATION: float = 10000

class EcosystemAction(enum.IntEnum):
    Rest = 0
    Reproduce = 1
    Hunt = 2

# Model parameters
class EcosystemModel():
    def __init__(self, ecosystem_configuration: EcosystemConfiguration = EcosystemConfiguration()):
        self.ecosystem_configuration = ecosystem_configuration
        self.reset()

    def reset(self,
             initial_lion_population: float = 0,
             initial_gazelle_population: float = 0
        ):
        self._lion_population = initial_lion_population
        self._gazelle_population = initial_gazelle_population
        self._lion_food = self._lion_population * self.ecosystem_configuration.LION_FOOD_CONSUMPTION # enough food for first step

    def step(self, command: float):
        # TODO: Apply probabilities to reproduction, hunting, death, etc. instead of just multiplying and rounding.

        if command == EcosystemAction.Reproduce:
            self._lion_population += math.floor(self._lion_population * self.ecosystem_configuration.LION_REPRODUCE_BIRTH_RATE)
        elif command == EcosystemAction.Hunt:
            kills = math.floor(min(self._lion_population * self.ecosystem_configuration.LION_HUNT_RATE, self._gazelle_population))
            self._lion_food += kills
            self._gazelle_population -= kills
        
        self._lion_population -= math.floor(self._lion_population * self.ecosystem_configuration.LION_DEATH_RATE)
        if self.ecosystem_configuration.LION_FOOD_CONSUMPTION > 0:
            self._lion_population = math.floor(min(self._lion_population, self._lion_food / self.ecosystem_configuration.LION_FOOD_CONSUMPTION))
        self._lion_food -= self._lion_population * self.ecosystem_configuration.LION_FOOD_CONSUMPTION
        self._lion_population = min(self._lion_population, self.ecosystem_configuration.MAXIMUM_LION_POPULATION)

        self._gazelle_population += math.floor(self._gazelle_population * self.ecosystem_configuration.GAZELLE_NET_REPRODUCE_RATE)
        self._gazelle_population = min(self._gazelle_population, self.ecosystem_configuration.MAXIMUM_GAZELLE_POPULATION)
