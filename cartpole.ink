# This sample demonstrates how to teach a policy for controlling
# a cartpole (inverted pendulum) device.

inkling "2.0"

using Math
using Goal

# Desired lion population
const MinimumLionPopulation = 1000
const MaximumLionPopulation = 2000

# Type that represents the per-iteration state returned by simulator
type SimState {
    # Population of lions
    lion_population: number,
}

# Type that represents the per-iteration action accepted by the simulator
type SimAction {
    # Behavior of lions in the next time step
    command: number<Rest = 0, Reproduce = 1>
}

# Define a type that represents the per-episode configuration
# settings supported by the simulator.
type SimConfig {
    # Starting cart position in meters
    initial_lion_population: number<0 .. 100000>,
}

# Define a concept graph with a single concept
graph (input: SimState): SimAction {
    concept BalanceEcosystem(input): SimAction {
        curriculum {
            # The source of training for this concept is a simulator
            # that takes an action as an input and outputs a state.
            source simulator (Action: SimAction, Config: SimConfig): SimState {
            }

            # The objective of training is a goal of a particular lion population.
            goal (State: SimState) {
                drive LionPopulation:
                    State.lion_population in Goal.Range(MinimumLionPopulation, MaximumLionPopulation)
            }

            training {
                # Limit the number of iterations per episode to 120. The default
                # is 1000, which makes it much tougher to succeed.
                EpisodeIterationLimit: 120
            }

            lesson BasicLesson {
                scenario {
                    initial_lion_population: number<10 .. 10000>
                }
            }
        }
    }
}
