import numpy as np
from time import sleep

from snakegame import SnakeGame
from nn import Network
from settings import *

class Member:
    __slots__ = "fitness", "model"
    def __init__(self, weights=None, biases=None):
        self.fitness = 0
        
        nn_architecture = NN_ARQ
        self.model = Network(nn_architecture, weights, biases)

    def iterate_to_update_fitness(self, iterations=1):
        results = []
        for _ in range(iterations):
            result = self.play_game_to_update_fitness()
            results.append(result)
        self.fitness = int(sum(results)/len(results))
        return self.fitness

    def play_game_to_update_fitness(self, print_test=False):
        sg = SnakeGame()
        while(sg.alive):
            input = sg.get_current_input()
            next_move = self.next_move_from_input(input)
            sg.move_snake(next_move, print_test=print_test)
            if print_test:
                print(f"fitness:{sg.get_fitness_score()}")  
                sg.print_board()
                sleep(0.05)  
        self.fitness = sg.get_fitness_score()
        if print_test:
            print("THE_END")
            print(f"apple:{sg.apple_position}")
            print(f"snake:{sg.snake}")
            print(f"fitnes:{self.fitness}")
        return self.fitness

    def next_move_from_input(self, input):
        return np.argmax(self.model.feedforward(input))

