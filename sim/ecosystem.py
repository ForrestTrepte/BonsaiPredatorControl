# pyright: strict

import math
import random
import enum

class EcosystemConfiguration():
    lion_reproduce_birth_rate: float = 0.25
    lion_death_rate: float = 0.1
    lion_hunt_rate: float = 0.5 # number of gazelles killed per lion hunting
    lion_food_consumption: float = 0.1 # number of gazelles eaten per lion
    maximum_lion_food: float = 10000
    maximum_lion_population: float = 10000
    gazelle_net_reproduce_rate: float = 0.1
    gazelle_food_consumption: float = 0.1
    maximum_gazelle_population: float = 10000
    grass_net_reproduce_rate: float = 0.1
    maximum_grass_population: float = 10000

class EcosystemModel():
    def __init__(self, ecosystem_configuration: EcosystemConfiguration = EcosystemConfiguration()):
        self.ecosystem_configuration = ecosystem_configuration
        self.reset(0, 0, 0)

    def reset(self,
             initial_lion_population: float,
             initial_gazelle_population: float,
             initial_grass_population: float):
        self._lion_population = initial_lion_population
        self._gazelle_population = initial_gazelle_population
        self._lion_food = self._lion_population * self.ecosystem_configuration.lion_food_consumption # enough food for first step
        self._grass_population = initial_grass_population

    def step(self, reproduction: float, hunting: float):
        assert 0.0 <= reproduction <= 1.0
        assert 0.0 <= hunting <= 1.0

        # TODO: Apply probabilities to reproduction, hunting, death, etc. instead of just multiplying and rounding.

        # Reproduction
        self._lion_population += math.floor(self._lion_population * self.ecosystem_configuration.lion_reproduce_birth_rate * reproduction)

        # Hunting
        kills = math.floor(min(self._lion_population * self.ecosystem_configuration.lion_hunt_rate * hunting, self._gazelle_population))
        self._lion_food += kills
        self._gazelle_population -= kills

        # Death
        self._lion_population -= math.floor(self._lion_population * self.ecosystem_configuration.lion_death_rate)

        # Food
        if self.ecosystem_configuration.lion_food_consumption > 0:
            self._lion_population = min(self._lion_population, math.floor(self._lion_food / self.ecosystem_configuration.lion_food_consumption))
        self._lion_food -= self._lion_population * self.ecosystem_configuration.lion_food_consumption
        self._lion_food = min(self._lion_food, self.ecosystem_configuration.maximum_lion_food)

        # Maximum Population
        self._lion_population = min(self._lion_population, self.ecosystem_configuration.maximum_lion_population)

        # Gazelles
        self._gazelle_population += math.floor(self._gazelle_population * self.ecosystem_configuration.gazelle_net_reproduce_rate)
        if self.ecosystem_configuration.gazelle_food_consumption > 0:
            self._gazelle_population = min(self._gazelle_population, math.floor(self._grass_population / self.ecosystem_configuration.gazelle_food_consumption))
        self._grass_population -= math.ceil(self._gazelle_population * self.ecosystem_configuration.gazelle_food_consumption)
        self._gazelle_population = min(self._gazelle_population, self.ecosystem_configuration.maximum_gazelle_population)

        # Grass
        self._grass_population += math.floor(self._grass_population * self.ecosystem_configuration.grass_net_reproduce_rate)
        self._grass_population = min(self._grass_population, self.ecosystem_configuration.maximum_grass_population)
