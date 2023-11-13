from enum import Enum

## Processing
PARALLEL_CPU = 1

## Genetic Algorithm Config
POPULATION_SIZE = 1000
GENERATIONS = 1000
ITERATIONS_PER_GENERATION = 7
RANDOM_MEMBERS_TO_ADD = 100
MUTATION_RATE = 80
TOP_PARENTS_SELECTED = 50
ADD_PARENTS = True
CROSSOVERS_TO_ADD = 900

## Neural Network Config
INPUT_SIZE = 10
OUTPUT_SIZE = 3
NEURONS_PER_LAYER = 25
NN_ARQ = [
            {"input_dim": INPUT_SIZE, "output_dim": NEURONS_PER_LAYER, "activation": "relu"},
            {"input_dim": NEURONS_PER_LAYER, "output_dim": OUTPUT_SIZE, "activation": "sigmoid"},
        ]

#  Game Config
BOARD_SIZE = 18
MAX_STEPS_WITHOUT_FOOD = 6 * BOARD_SIZE #6 * BOARD_SIZE * BOARD_SIZE #int(BOARD_SIZE * BOARD_SIZE / 2) #5 * BOARD_SIZE * BOARD_SIZE

################ End Config #################

class Output(Enum):
    LEFT = 0
    STRAIGHT = 1
    RIGHT = 2

class BoardCell(Enum):
    EMPTY = 0
    WALL = 1
    SNAKE = 2
    FRUIT = 3

class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

"""
Run results:
np.random.randn is much better than np.random.uniform (in Member as initia nn weights and biases)
--> 150K-300K vs 500K-1M

Pending results:
Generate fixed initial Popultaion
Remove random members
Remove parents?
then:
Test Mutation Rate
Test Iterations per generation
Test Top parents selected


x86, no jit
40.59 max:474848 avg top 10:410711
31.40 max:253140 avg top 10:211222

x86, with jit
28.67 max:507201 avg top 10:341259
26.99 max:365869 avg top 10:215231


"""