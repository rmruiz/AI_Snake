from dna import Dna
import json
import jsonpickle
from json import JSONEncoder

FILENAME = "winner.json"

if __name__ == '__main__':
    member = Dna(1)

    with open(FILENAME, 'r', encoding='utf-8') as f:
        json_data = json.load(f)

    data = jsonpickle.decode(json_data)

    member.model.sizes = data['sizes']
    member.model.biases = data['biases']
    member.model.weights = data['weights']
    member.model.num_layers = len(member.model.sizes)

    member.test_dna_to_update_fitness(print_test=True)
    
    

        