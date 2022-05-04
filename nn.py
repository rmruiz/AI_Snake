#https://towardsdatascience.com/lets-code-a-neural-network-in-plain-numpy-ae7e74410795
import numpy as np

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

def single_layer_forward_propagation(A, W, b, activation="relu"):
    
    if activation == "relu":
        activation_func = relu
    elif activation == "sigmoid":
        activation_func = sigmoid
    else:
        raise Exception('Non-supported activation function')
        
    return activation_func(np.dot(W, A) + b)


if __name__ == '__main__':
    nn_architecture = [
        {"input_dim": 4, "output_dim": 6, "activation": "relu"},
        {"input_dim": 6, "output_dim": 3, "activation": "sigmoid"},
    ]
    my_network = Network(nn_architecture)

    result = my_network.feedforward([[0.3], [0.4], [-0.2], [-1]])

    print(f"result={result}")