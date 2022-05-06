from enum import Enum

## Genetic Algorithm Config
POPULATION_SIZE = 4#2000
GENERATIONS = 2#100
ITERATIONS_PER_GENERATION = 1#10
RANDOM_MEMBERS_TO_ADD = 0#5
MUTATION_RATE = 0#80
TOP_PARENTS_SELECTED = 2#200
ADD_PARENTS = False#True
CROSSOVERS_TO_ADD = 4#1800

## Neural Network Config
INPUT_SIZE = 17
OUTPUT_SIZE = 3
NEURONS_PER_LAYER = 25
NN_ARQ = [
            {"input_dim": INPUT_SIZE, "output_dim": NEURONS_PER_LAYER, "activation": "relu"},
            {"input_dim": NEURONS_PER_LAYER, "output_dim": OUTPUT_SIZE, "activation": "sigmoid"},
        ]

#  Game Config
BOARD_SIZE = 18
MAX_STEPS_WITHOUT_FOOD = 400 #int(BOARD_SIZE * BOARD_SIZE / 2) #5 * BOARD_SIZE * BOARD_SIZE

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