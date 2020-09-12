# PredatorControl

Teaches a policy for controlling a toy ecosystem simulation with a population of lions and gazelles.
Created as an exercise for learning Bonsai. This is based on the [cartpole-py](https://github.com/microsoft/cartpole-py) sample.

# How to Run

* Run tests by installing and executing `pytest`.
* Run locally by setting the environment variables `SIM_ACCESS_KEY` and `SIM_WORKSPACE`. Then execute `python __main__.py`.
* Build and push a simulator container by executing `BuildAndPushContainer.bat`.
* Train the simulation using the online Bonsai workspace, creating a Brain and pasting the contents of [predator_control.ink](/predator_control.ink) into the Train tab.
