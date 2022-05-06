import numpy as np
import timeit
from functools import partial

def relu(z):
    return np.maximum(0,z)

def sigmoid(z):
    """The sigmoid function."""
    return 1.0/(1.0+np.exp(-z))

class Network():
    def __init__(self, nn_architecture, weights=None, biases=None):
        self.nn_architecture = nn_architecture
   
        if weights is None:
            self.weights = []
            for layer in nn_architecture:
                layer_input_size = layer["input_dim"]
                layer_output_size = layer["output_dim"]
                self.weights.append(np.random.randn(layer_output_size,layer_input_size))
                #TODO:test uniform distrib
                #self.weights.append(np.random.uniform(low=-1.0, high=1.0, 
                #    size=(layer_output_size,layer_input_size)))
        else:
            self.weights = weights
                
        if biases is None:
            self.biases = []
            for layer in nn_architecture:
                layer_output_size = layer["output_dim"]
                self.biases.append(np.random.randn(layer_output_size,1))
                #TODO:test uniform distrib
                #self.biases.append(np.random.uniform(low=-1.0, high=1.0, 
                #    size=(layer_output_size,1)))
        else:
            self.biases = biases
            
    def feedforward(self, A):
        for idx, layer in enumerate(self.nn_architecture):
            activ_function = layer["activation"]
            W = self.weights[idx]
            b = self.biases[idx]
            A = single_layer_forward_propagation(A, W, b, activ_function)
        return A

class NetworkWithSlots():
    __slots__ = "nn_architecture", "weights", "biases"
    def __init__(self, nn_architecture, weights=None, biases=None):
        self.nn_architecture = nn_architecture
   
        if weights is None:
            self.weights = []
            for layer in nn_architecture:
                layer_input_size = layer["input_dim"]
                layer_output_size = layer["output_dim"]
                self.weights.append(np.random.randn(layer_output_size,layer_input_size))
                #TODO:test uniform distrib
                #self.weights.append(np.random.uniform(low=-1.0, high=1.0, 
                #    size=(layer_output_size,layer_input_size)))
        else:
            self.weights = weights
                
        if biases is None:
            self.biases = []
            for layer in nn_architecture:
                layer_output_size = layer["output_dim"]
                self.biases.append(np.random.randn(layer_output_size,1))
                #TODO:test uniform distrib
                #self.biases.append(np.random.uniform(low=-1.0, high=1.0, 
                #    size=(layer_output_size,1)))
        else:
            self.biases = biases
            
    def feedforward(self, A):
        for idx, layer in enumerate(self.nn_architecture):
            activ_function = layer["activation"]
            W = self.weights[idx]
            b = self.biases[idx]
            A = single_layer_forward_propagation(A, W, b, activ_function)
        return A

def single_layer_forward_propagation(A, W, b, activation="relu"):
    
    if activation == "relu":
        activation_func = relu
    elif activation == "sigmoid":
        activation_func = sigmoid
    else:
        raise Exception('Non-supported activation function')
        
    return activation_func(np.dot(W, A) + b)


if __name__ == '__main__':
    
    input = [[0.3], [0.4], [-0.2], [-1]]
    nn_architecture = [
        {"input_dim": 4, "output_dim": 6, "activation": "relu"},
        {"input_dim": 6, "output_dim": 3, "activation": "sigmoid"},
    ]
    n1 = Network(nn_architecture)
    n2 = NetworkWithSlots(nn_architecture)

    iterations = 100000
    no_slots = min(timeit.repeat(partial(n1.feedforward, input), number=iterations))
    slots = min(timeit.repeat(partial(n2.feedforward, input), number=iterations))
    print(f"no slots:{no_slots}")
    print(f"slots:{slots}")
    print(f"Perf Improvement: {(no_slots-slots)/no_slots:.2%}")