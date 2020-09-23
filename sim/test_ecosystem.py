import ecosystem

def get_test_ecosystem_configuration() -> ecosystem.EcosystemConfiguration:
    config = ecosystem.EcosystemConfiguration()
    config.lion_reproduce_birth_rate = 0
    config.lion_death_rate = 0
    config.lion_hunt_rate = 0
    config.lion_food_consumption = 0
    config.maximum_lion_population = 1000000
    config.gazelle_net_reproduce_rate = 0
    config.gazelle_food_consumption = 0
    config.maximum_gazelle_population = 1000000
    config.grass_net_reproduce_rate = 0
    config.maximum_grass_population = 100000
    return config

def test_init_sim():
    test_ecosystem_configuration = get_test_ecosystem_configuration()
    model = ecosystem.EcosystemModel(test_ecosystem_configuration)
    assert model.ecosystem_configuration == test_ecosystem_configuration
    assert model._lion_population == 0
    assert model._lion_food == 0
    assert model._gazelle_population == 0
    assert model._grass_population == 0
    model.reset(1, 2, 3)
    assert model._lion_population == 1
    assert model._gazelle_population == 2
    assert model._grass_population == 3

def test_reproduce():
    test_ecosystem_configuration = get_test_ecosystem_configuration()
    test_ecosystem_configuration.lion_reproduce_birth_rate = 0.1
    test_ecosystem_configuration.maximum_lion_population = 109
    test_ecosystem_configuration.gazelle_net_reproduce_rate = 0.2
    test_ecosystem_configuration.maximum_gazelle_population = 1441
    test_ecosystem_configuration.grass_net_reproduce_rate = 0.3
    test_ecosystem_configuration.maximum_grass_population = 3381
    model = ecosystem.EcosystemModel(test_ecosystem_configuration)
    model.reset(100, 1000, 2000)
    assert model._lion_population == 100
    assert model._gazelle_population == 1000
    assert model._grass_population == 2000

    # reproduce without lion reproduction
    model.step(0.0, 0.0)
    assert model._lion_population == 100
    assert model._gazelle_population == 1200
    assert model._grass_population == 2600

    # reproduce with 80% lion reproduction
    model.step(0.8, 0.0)
    assert model._lion_population == 108
    assert model._gazelle_population == 1440
    assert model._grass_population == 3380

    # reproduce capped by maximum population
    model.step(1.0, 0.0)
    assert model._lion_population == 109
    assert model._gazelle_population == 1441
    assert model._grass_population == 3381

def test_lion_death():
    test_ecosystem_configuration = get_test_ecosystem_configuration()
    test_ecosystem_configuration.lion_death_rate = 0.1
    model = ecosystem.EcosystemModel(test_ecosystem_configuration)
    model.reset(100, 0, 0)
    assert model._lion_population == 100
    model.step(0.0, 0.0)
    assert model._lion_population == 90

def test_lion_food():
    test_ecosystem_configuration = get_test_ecosystem_configuration()
    test_ecosystem_configuration.lion_food_consumption = 0.1
    model = ecosystem.EcosystemModel(test_ecosystem_configuration)
    model.reset(100, 0, 0)
    assert model._lion_food == 10
    assert model._lion_population == 100
    model.step(0.0, 0.0)
    assert model._lion_food == 0
    assert model._lion_population == 100
    model.step(0.0, 0.0)
    assert model._lion_food == 0
    assert model._lion_population == 0

def test_gazelle_food():
    test_ecosystem_configuration = get_test_ecosystem_configuration()
    test_ecosystem_configuration.gazelle_food_consumption = 0.1
    model = ecosystem.EcosystemModel(test_ecosystem_configuration)
    model.reset(0, 100, 15)
    assert model._gazelle_population == 100
    assert model._grass_population == 15
    model.step(0.0, 0.0)
    assert model._gazelle_population == 100
    assert model._grass_population == 5
    model.step(0.0, 0.0)
    assert model._gazelle_population == 50
    assert model._grass_population == 0

def test_hunt():
    test_ecosystem_configuration = get_test_ecosystem_configuration()
    test_ecosystem_configuration.lion_hunt_rate = 0.1
    test_ecosystem_configuration.maximum_lion_food = 9
    model = ecosystem.EcosystemModel(test_ecosystem_configuration)
    model.reset(100, 1000, 0)
    assert model._lion_food == 0
    assert model._lion_population == 100
    assert model._gazelle_population == 1000

    # step without lion hunting
    model.step(0.0 ,0.0)
    assert model._lion_food == 0
    assert model._lion_population == 100
    assert model._gazelle_population == 1000

    # step with 80% lion hunting
    model.step(0.0, 0.8)
    assert model._lion_food == 8
    assert model._lion_population == 100
    assert model._gazelle_population == 992

    # excess of maximum food is lost
    model.step(0.0, 0.8)
    assert model._lion_food == 9
    assert model._lion_population == 100
    assert model._gazelle_population == 984

def is_whole_number(value):
    if type(value) == int:
        return True
    return value.is_integer()

def test_sustainable_default_configuration():
    # verify that a stable state is possible where all populations rise using the default configuration
    config = ecosystem.EcosystemConfiguration()
    model = ecosystem.EcosystemModel(config)

    # this may need to be adjusted whenever the base simulation is changed
    model.reset(1000, 3000, 9000)
    initial_lion_population = model._lion_population
    initial_lion_food = model._lion_food
    initial_gazelle_population = model._gazelle_population
    initial_grass_population = model._grass_population
    reproduce_slightly_above_death_rate = (config.lion_death_rate + 0.05) / config.lion_reproduce_birth_rate
    hunt_slightly_above_food_consumption = (config.lion_food_consumption + 0.05) / config.lion_hunt_rate
    model.step(reproduce_slightly_above_death_rate, hunt_slightly_above_food_consumption)
    assert model._lion_population > initial_lion_population
    assert is_whole_number(model._lion_population)
    assert model._lion_food > initial_lion_food
    assert model._gazelle_population > initial_gazelle_population
    assert is_whole_number(model._gazelle_population)
    assert model._grass_population > initial_grass_population
    assert is_whole_number(model._grass_population)
