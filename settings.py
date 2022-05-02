from enum import Enum
## Genetic Algorithm Config
POPULATION_SIZE = 2000
GENERATIONS = 100
ITERATIONS_PER_GENERATION = 4
RANDOM_MEMBERS_TO_ADD = 0
MUTATION_RATE = 70
TOP_PARENTS_SELECTED = 200
ADD_PARENTS = False
CROSSOVERS_TO_ADD = 2000

## Neural Network Config

INPUT_SIZE = 13
OUTPUT_SIZE = 3
NEURONS_HIDDEN_LAYERS = 18
NEURONS_PER_LAYER = 6

class Output(Enum):
    LEFT = 0
    STRAIGHT = 1
    RIGHT = 2