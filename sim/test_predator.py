import cartpole

def get_test_ecosystem_configuration() -> cartpole.EcosystemConfiguration:
    config = cartpole.EcosystemConfiguration()
    config.LION_REPRODUCE_BIRTH_RATE = 0
    config.LION_DEATH_RATE = 0
    config.LION_HUNT_RATE = 0
    config.LION_FOOD_CONSUMPTION = 0
    config.MAXIMUM_LION_POPULATION = 1000000
    config.GAZELLE_NET_REPRODUCE_RATE = 0
    config.MAXIMUM_GAZELLE_POPULATION = 1000000
    return config

def test_init_sim():
    test_ecosystem_configuration = get_test_ecosystem_configuration()
    model = cartpole.CartPoleModel(test_ecosystem_configuration)
    assert model.ecosystem_configuration == test_ecosystem_configuration
    assert model._lion_population == 0
    assert model._lion_food == 0
    assert model._gazelle_population == 0
    model.reset(1, 2)
    assert model._lion_population == 1
    assert model._gazelle_population == 2

def test_reproduce():
    test_ecosystem_configuration = get_test_ecosystem_configuration()
    test_ecosystem_configuration.LION_REPRODUCE_BIRTH_RATE = 0.1
    test_ecosystem_configuration.MAXIMUM_LION_POPULATION = 111
    test_ecosystem_configuration.GAZELLE_NET_REPRODUCE_RATE = 0.2
    test_ecosystem_configuration.MAXIMUM_GAZELLE_POPULATION = 1441
    model = cartpole.CartPoleModel(test_ecosystem_configuration)
    model.reset(100, 1000)
    assert model._lion_population == 100
    assert model._gazelle_population == 1000

    # reproduce without lion reproduction
    model.step(cartpole.EcosystemAction.Rest)
    assert model._lion_population == 100
    assert model._gazelle_population == 1200

    # reproduce with lion reproduction
    model.step(cartpole.EcosystemAction.Reproduce)
    assert model._lion_population == 110
    assert model._gazelle_population == 1440

    # reproduce capped by maximum population
    model.step(cartpole.EcosystemAction.Reproduce)
    assert model._lion_population == 111
    assert model._gazelle_population == 1441

def test_lion_death():
    test_ecosystem_configuration = get_test_ecosystem_configuration()
    test_ecosystem_configuration.LION_DEATH_RATE = 0.1
    model = cartpole.CartPoleModel(test_ecosystem_configuration)
    model.reset(100, 0)
    assert model._lion_population == 100
    model.step(cartpole.EcosystemAction.Rest)
    assert model._lion_population == 90

def test_lion_food():
    test_ecosystem_configuration = get_test_ecosystem_configuration()
    test_ecosystem_configuration.LION_FOOD_CONSUMPTION = 0.1
    model = cartpole.CartPoleModel(test_ecosystem_configuration)
    model.reset(100, 0)
    assert model._lion_food == 10
    assert model._lion_population == 100
    model.step(cartpole.EcosystemAction.Rest)
    assert model._lion_food == 0
    assert model._lion_population == 100
    model.step(cartpole.EcosystemAction.Rest)
    assert model._lion_food == 0
    assert model._lion_population == 0

def test_hunt():
    test_ecosystem_configuration = get_test_ecosystem_configuration()
    test_ecosystem_configuration.LION_HUNT_RATE = 0.1
    model = cartpole.CartPoleModel(test_ecosystem_configuration)
    model.reset(100, 1000)
    assert model._lion_food == 0
    assert model._lion_population == 100
    assert model._gazelle_population == 1000

    # step without lion hunting
    model.step(cartpole.EcosystemAction.Rest)
    assert model._lion_food == 0
    assert model._lion_population == 100
    assert model._gazelle_population == 1000

    # step with lion hunting
    model.step(cartpole.EcosystemAction.Hunt)
    assert model._lion_food == 10
    assert model._lion_population == 100
    assert model._gazelle_population == 990
