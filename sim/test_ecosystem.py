import ecosystem

def get_test_ecosystem_configuration() -> ecosystem.EcosystemConfiguration:
    config = ecosystem.EcosystemConfiguration()
    config.lion_reproduce_birth_rate = 0
    config.lion_death_rate = 0
    config.lion_hunt_rate = 0
    config.lion_food_consumption = 0
    config.maximum_lion_population = 1000000
    config.gazelle_net_reproduce_rate = 0
    config.maximum_gazelle_population = 1000000
    return config

def test_init_sim():
    test_ecosystem_configuration = get_test_ecosystem_configuration()
    model = ecosystem.EcosystemModel(test_ecosystem_configuration)
    assert model.ecosystem_configuration == test_ecosystem_configuration
    assert model._lion_population == 0
    assert model._lion_food == 0
    assert model._gazelle_population == 0
    model.reset(1, 2)
    assert model._lion_population == 1
    assert model._gazelle_population == 2

def test_reproduce():
    test_ecosystem_configuration = get_test_ecosystem_configuration()
    test_ecosystem_configuration.lion_reproduce_birth_rate = 0.1
    test_ecosystem_configuration.maximum_lion_population = 109
    test_ecosystem_configuration.gazelle_net_reproduce_rate = 0.2
    test_ecosystem_configuration.maximum_gazelle_population = 1441
    model = ecosystem.EcosystemModel(test_ecosystem_configuration)
    model.reset(100, 1000)
    assert model._lion_population == 100
    assert model._gazelle_population == 1000

    # reproduce without lion reproduction
    model.step(0.0, 0.0)
    assert model._lion_population == 100
    assert model._gazelle_population == 1200

    # reproduce with 80% lion reproduction
    model.step(0.8, 0.0)
    assert model._lion_population == 108
    assert model._gazelle_population == 1440

    # reproduce capped by maximum population
    model.step(1.0, 0.0)
    assert model._lion_population == 109
    assert model._gazelle_population == 1441

def test_lion_death():
    test_ecosystem_configuration = get_test_ecosystem_configuration()
    test_ecosystem_configuration.lion_death_rate = 0.1
    model = ecosystem.EcosystemModel(test_ecosystem_configuration)
    model.reset(100, 0)
    assert model._lion_population == 100
    model.step(0.0, 0.0)
    assert model._lion_population == 90

def test_lion_food():
    test_ecosystem_configuration = get_test_ecosystem_configuration()
    test_ecosystem_configuration.lion_food_consumption = 0.1
    model = ecosystem.EcosystemModel(test_ecosystem_configuration)
    model.reset(100, 0)
    assert model._lion_food == 10
    assert model._lion_population == 100
    model.step(0.0, 0.0)
    assert model._lion_food == 0
    assert model._lion_population == 100
    model.step(0.0, 0.0)
    assert model._lion_food == 0
    assert model._lion_population == 0

def test_hunt():
    test_ecosystem_configuration = get_test_ecosystem_configuration()
    test_ecosystem_configuration.lion_hunt_rate = 0.1
    model = ecosystem.EcosystemModel(test_ecosystem_configuration)
    model.reset(100, 1000)
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
