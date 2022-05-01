exit()
import numpy as np
#import random
#import pickle
#import gzip

#https://gist.github.com/roycoding/7bfcd821ae5be40804979973be149953

def relu(z):
    return np.maximum(0,z)

def sigmoid(z):
    """The sigmoid function."""
    return 1.0/(1.0+np.exp(-z))

def sigmoid_prime(z):
    """Derivative of the sigmoid function."""
    return sigmoid(z)*(1-sigmoid(z))

class Network(object):

    def __init__(self, sizes):
        """The list ``sizes`` contains the number of neurons in the
        respective layers of the network.  For example, if the list
        was [2, 3, 1] then it would be a three-layer network, with the
        first layer containing 2 neurons, the second layer 3 neurons,
        and the third layer 1 neuron.  The biases and weights for the
        network are initialized randomly, using a Gaussian
        distribution with mean 0, and variance 1.  Note that the first
        layer is assumed to be an input layer, and by convention we
        won't set any biases for those neurons, since biases are only
        ever used in computing the outputs from later layers."""
        
        self.num_layers = len(sizes)
        self.sizes = sizes

        self.biases = [np.random.randn(y, 1) for y in sizes[1:]]
        self.weights = [np.random.randn(y, x) for x, y in zip(sizes[:-1], sizes[1:])]
        #self.biases = [np.random.uniform(low=-1.0, high=1.0, size=(y,1)) for y in sizes[1:]]
        #self.weights = [np.random.uniform(low=-1.0, high=1.0, size=(y,x)) for x, y in zip(sizes[:-1], sizes[1:])]

    def feedforward(self, a):
        """Return the output of the network if ``a`` is input."""
        
        for b, w in zip(self.biases, self.weights):
            #print(f"size w: {np.array(w).shape}")
            #print(f"W:{w}")
            
            #print(f"lenght a: {np.array(a).shape}")
            #print(f"A:{a}")
        
            #print(f"lenght b: {np.array(b).shape}")
            #print(f"B:{b}")
            #print("")

            #print(f"lenght wa: {np.array(np.dot(w, a)).shape}")
            #print(f"lenght wa+b: {np.array(np.dot(w, a)+b).shape}")

            a = sigmoid(np.dot(w, a)+b)
            #print(a)
        #print(f"lenght a: {np.array(a).shape}")
        return a

if __name__ == '__main__':
    #my_network = Network([4,3,6,1])
    my_network = Network([4,6,3])

    a = np.random.random(size=(4,1))
    a = np.random.uniform(low=-1.0, high=1.0, size=(4,1))

    result = my_network.feedforward(a)

    print(f"result={result}")

    #print(f"weights={my_network.weights}")

    #print(f"biases={my_network.biases}")