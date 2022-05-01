import numpy as np

from time import sleep
from enum import Enum

from snakegame import SnakeGame
from nn2 import Network

INPUT_SIZE = 13
OUTPUT_SIZE = 3
HIDDEN_LAYERS = 1
NEURONS_PER_LAYER = 6

class Output(Enum):
    LEFT = 0
    STRAIGHT = 1
    RIGHT = 2

class Dna:
    #creates a random DNA
    def __init__(self, id, empty=False):
        self.id = id
        self.model = None
        self.fitness = 0
        
        nn_architecture = [
            {"input_dim": INPUT_SIZE, "output_dim": 18, "activation": "relu"},
            {"input_dim": 18, "output_dim": OUTPUT_SIZE, "activation": "sigmoid"},
        ]
        self.model = Network(nn_architecture, empty)
        #print('D', end='', flush=True)

    #def get_weights(self):
    #    return self.model.weights

    def iterate_to_update_fitness(self, iterations=1):
        results = []
        for i in range(iterations):
            result = self.test_dna_to_update_fitness()
            results.append(result)
        self.fitness = int(sum(results)/len(results))

    def test_dna_to_update_fitness(self, print_test=False):

        sg = SnakeGame()
        while(sg.alive):
            input = sg.get_current_input()
            if print_test:
                print(input)
            #check next move
            next_move = self.next_move_from_input(input)
            #print(f"{next_move=}")
            sg.move_snake(next_move, print_test=print_test)
            if print_test:
                print(f"fitness:{sg.get_fitness_score()}")  
                sg.print_board()
                sleep(0.6)  
        #calculate new fitness
        self.fitness = sg.get_fitness_score()
        if print_test:
            print("THE_END")
            print(f"apple:{sg.apple_position}")
            print(f"snake:{sg.snake}")
            print(f"fitnes:{self.fitness}")
        return self.fitness

    def next_move_from_input(self, input):
        #prediction = self.model.predict([input])
        #print(f"input={input}")
        #print(f"input.shape={np.array(input).shape}")
        prediction = self.model.feedforward(input)
        
        #print(f"prediction={prediction}")
        #print(f"prediction.shape={np.array(prediction).shape}")
        #print(prediction)
        return np.argmax(prediction)

