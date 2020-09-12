# pyright: strict

import math
import random
import enum

class EcosystemConfiguration():
    lion_reproduce_birth_rate: float = 0.25
    lion_death_rate: float = 0.1
    lion_hunt_rate: float = 0.5 # number of gazelles killed per lion hunting
    lion_food_consumption: float = 0.1 # number of gazelles eaten per lion
    maximum_lion_population: float = 10000
    gazelle_net_reproduce_rate: float = 0.1
    maximum_gazelle_population: float = 10000

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
        self._lion_food = self._lion_population * self.ecosystem_configuration.lion_food_consumption # enough food for first step

    def step(self, command: float):
        # TODO: Apply probabilities to reproduction, hunting, death, etc. instead of just multiplying and rounding.

        if command == EcosystemAction.Reproduce:
            self._lion_population += math.floor(self._lion_population * self.ecosystem_configuration.lion_reproduce_birth_rate)
        elif command == EcosystemAction.Hunt:
            kills = math.floor(min(self._lion_population * self.ecosystem_configuration.lion_hunt_rate, self._gazelle_population))
            self._lion_food += kills
            self._gazelle_population -= kills
        
        self._lion_population -= math.floor(self._lion_population * self.ecosystem_configuration.lion_death_rate)
        if self.ecosystem_configuration.lion_food_consumption > 0:
            self._lion_population = math.floor(min(self._lion_population, self._lion_food / self.ecosystem_configuration.lion_food_consumption))
        self._lion_food -= self._lion_population * self.ecosystem_configuration.lion_food_consumption
        self._lion_population = min(self._lion_population, self.ecosystem_configuration.maximum_lion_population)

        self._gazelle_population += math.floor(self._gazelle_population * self.ecosystem_configuration.gazelle_net_reproduce_rate)
        self._gazelle_population = min(self._gazelle_population, self.ecosystem_configuration.maximum_gazelle_population)
