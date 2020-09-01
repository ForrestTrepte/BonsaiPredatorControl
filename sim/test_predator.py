from cartpole import CartPoleModel

def test_init_sim():
    cartpole = CartPoleModel()
    assert cartpole._lion_population == 0
    assert cartpole._lion_food == 0
    assert cartpole._gazelle_population == 0
    cartpole.reset(1, 2)
    assert cartpole._lion_population == 1
    assert cartpole._gazelle_population == 2
