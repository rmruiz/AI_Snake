#import os
#os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

#import tensorflow as tf
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
        self.model = Network([INPUT_SIZE, OUTPUT_SIZE,6 ,1])
        self.fitness = 0
        print(':', end='', flush=True)

    def get_weights(self):
        #return self.layer1.get_weights()
        return self.model.weights

    def get_next_move(self, input):
        if len(input) != INPUT_SIZE:
            raise "input size is invalid"
        #return self.model.predict([input])
        return self.model.feedforward(input)[0]

    def iterate_to_update_fitness(self, iterations=1):
        results = []
        for i in range(iterations):
            result = self.test_dna_to_update_fitness()
            results.append(result)
        self.fitness = int(sum(results)/len(results))

    def test_dna_to_update_fitness(self, print_test=False):

        sg = SnakeGame()
        #sg.print_board()
        while(sg.alive):
            input = sg.get_current_input()
            #check next move
            next_move = self.next_move_from_input(input)
            #print(f"{next_move=}")
            sg.move_snake(next_move, print_test=print_test)
            if print_test:
                print(f"fitness:{sg.get_fitness_score()}")    
        #calculate new fitness
        self.fitness = sg.get_fitness_score()
        if print_test:
            print("THE_END")
            print(f"apple:{sg.fruit_position}")
            print(f"snake:{sg.snake}")
        
        return self.fitness

    def next_move_from_input(self, input):
        #prediction = self.model.predict([input])
        prediction = self.model.feedforward(input)
        #print(prediction)
        if prediction[0][0] >= prediction[0][1]:
            if prediction[0][0] >= prediction[0][2]:
                if prediction[0][0] >= prediction[0][3]:
                    return "north"
        if prediction[0][1] >= prediction[0][0]:
            if prediction[0][1] >= prediction[0][2]:
                if prediction[0][1] >= prediction[0][3]:
                    return "south" 
        if prediction[0][2] >= prediction[0][0]:
            if prediction[0][2] >= prediction[0][1]:
                if prediction[0][2] >= prediction[0][3]:
                    return "west"
        if prediction[0][3] >= prediction[0][0]:
            if prediction[0][3] >= prediction[0][1]:
                if prediction[0][3] >= prediction[0][2]:
                    return "east"