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
    lion_food: number,
    gazelle_population: number,
    grass_population: number
}

# Type that represents the per-iteration action accepted by the simulator
type SimAction {
    # Behavior of lions in the next time step
    reproduction: number<0 .. 1>,
    hunting: number<0 .. 1>
}

# Define a type that represents the per-episode configuration
# settings supported by the simulator.
type SimConfig {
    initial_lion_population: number<0 .. 100000>,
    initial_gazelle_population: number<0 .. 100000>,
    initial_grass_population: number<0 .. 100000>
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
                avoid LionExtinction:
                    State.lion_population in Goal.RangeBelow(0)
            }

            training {
                EpisodeIterationLimit: 1000
            }

            lesson BasicLesson {
                scenario {
                    initial_lion_population: number<10 .. 10000>,
                    initial_gazelle_population: number<10 .. 10000>,
                    initial_grass_population: number<10 .. 10000>
                }
            }
        }
    }
}
