import numpy as np
from time import sleep
#from numba import jit #only for x86
#from numba import njit

from snakegame import SnakeGame
from settings import *

class Member:
    __slots__ = "fitness", "nn_architecture", "weights", "biases"
    
    def __init__(self, weights=None, biases=None):
        self.fitness = 0    
        self.nn_architecture = NN_ARQ
        if weights is None:
            self.random_weights()
        else:
            self.weights = weights
        if biases is None:
            self.random_biases()
        else:
            self.biases = biases

    def random_weights(self):
        self.weights = []
        for layer in self.nn_architecture:
            layer_input_size = layer["input_dim"]
            layer_output_size = layer["output_dim"]
            self.weights.append(np.random.randn(layer_output_size,layer_input_size))
            #TODO:test uniform distrib
            #self.weights.append(np.random.uniform(low=-1.0, high=1.0, 
            #    size=(layer_output_size,layer_input_size)))

    def random_biases(self):
        self.biases = []
        for layer in self.nn_architecture:
            layer_output_size = layer["output_dim"]
            self.biases.append(np.random.randn(layer_output_size,1))
            #TODO:test uniform distrib
            #self.biases.append(np.random.uniform(low=-1.0, high=1.0, 
            #    size=(layer_output_size,1)))

    def feedforward(self, A):
        for idx, layer in enumerate(self.nn_architecture):
            activ_function = layer["activation"]
            W = self.weights[idx]
            b = self.biases[idx]
            A = single_layer_forward_propagation(A, W, b, activ_function)
        return A

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
                print(f"fitness:{sg.get_score()}")  
                sg.print_board()
                sleep(0.05)  
        run_fitness = sg.get_score()
        if print_test:
            print("THE_END")
            print(f"apple:{sg.apple_position}")
            print(f"snake:{sg.snake}")
            print(f"fitnes:{run_fitness}")
        return sg.get_score()

    def next_move_from_input(self, input):
        return np.argmax(self.feedforward(input))

def single_layer_forward_propagation(A, W, b, activation="relu"):
    if activation == "relu":
        activation_func = relu
    elif activation == "sigmoid":
        activation_func = sigmoid
    else:
        raise Exception('Non-supported activation function')
        
    return activation_func(np.dot(W, A) + b)

#@njit(nopython=True)
def relu(z):
    return np.maximum(0,z)

#@njit(nopython=True)
def sigmoid(z):
    """The sigmoid function."""
    return 1.0/(1.0+np.exp(-z))