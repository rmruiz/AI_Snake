#import os
#os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

#import tensorflow as tf
from time import sleep
import numpy as np

from snakegame import SnakeGame

from nn import Network

INPUT_SIZE = 8
OUTPUT_SIZE = 4
HIDDEN_LAYERS = 1
NEURONS_PER_LAYER = 6
import warnings

class Dna:
    #creates a random DNA
    def __init__(self, id):
        self.id = id
        #self.layer1 = tf.keras.layers.Dense(units=NEURONS_PER_LAYER, input_shape=[INPUT_SIZE], name='dense1')
        #self.layerout = tf.keras.layers.Dense(units=OUTPUT_SIZE, name='denseout')
        #self.model = tf.keras.Sequential([self.layer1, self.layerout])
        self.model = Network([INPUT_SIZE, 6, OUTPUT_SIZE])
        self.fitness = 0
        self.name = str(id)
        #print(':', end='', flush=True)

    def get_weights(self):
        #return self.layer1.get_weights()
        return self.model.weights

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
                sleep(1)  
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
        if prediction[0][0] >= prediction[1][0]:
            if prediction[0][0] >= prediction[2][0]:
                if prediction[0][0] >= prediction[3][0]:
                    return "north"
        if prediction[1][0] >= prediction[0][0]:
            if prediction[1][0] >= prediction[2][0]:
                if prediction[1][0] >= prediction[3][0]:
                    return "south" 
        if prediction[2][0] >= prediction[0][0]:
            if prediction[2][0] >= prediction[1][0]:
                if prediction[2][0] >= prediction[3][0]:
                    return "west"
        if prediction[3][0] >= prediction[0][0]:
            if prediction[3][0] >= prediction[1][0]:
                if prediction[3][0] >= prediction[2][0]:
                    return "east"