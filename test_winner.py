from dna import Dna
import json
import jsonpickle
from json import JSONEncoder

FILENAME = "winner.json"

def test2():
    input = [[-1.0], [0.0], [0.5], [-1.0], [-1.0], [-1.0], [-1.0], [0.5], [-0.25]]
    for _ in range(50):
        member = Dna()
        print(member.next_move_from_input(input))        
           
def test1():
    member = Dna(1)

    with open(FILENAME, 'r', encoding='utf-8') as f:
        json_data = json.load(f)

    data = jsonpickle.decode(json_data)

    member.model.nn_architecture = data['nn_architecture']
    member.model.biases = data['biases']
    member.model.weights = data['weights']
    #member.model.num_layers = len(member.model.sizes)

    member.test_dna_to_update_fitness(print_test=True)
    
if __name__ == '__main__':
    test1()

        