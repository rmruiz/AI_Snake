from random import randint
from dna import Dna
import numpy as np

class Population:
    def __init__(self, size):
        self.next_id = 0
        self.members = []
        for _ in range(size):
            self.add_random_member()

    def add_random_member(self):
        self.members.append(Dna(self.next_id))
        self.next_id = self.next_id + 1

    def add_member_from_dna(self, dna):
        member = Dna(self.next_id)
        #model.get_layer(layerName).set_weights(...)
        member.model.get_layer("dense1").set_weights(dna)
        self.members.append(member)
        self.next_id = self.next_id + 1

    def fill_with_random_members(self, total_members):
        while(len(self.members) <= total_members):
            self.add_random_member()

    def crossover_50_50(self, parents, quantity, max_population):
        for _ in range(quantity):
            if len(self.members) >= max_population:
                break
            #print(f"starting crossover")
            father_id = parents[randint(0,len(parents)-1)]
            while True:
                mother_id = parents[randint(0,len(parents)-1)]
                if father_id != mother_id:
                    break
            #print(f"found a match! father:{father_id}, mother:{mother_id}")

            father_idx = mother_idx = -1
            for index, member in enumerate(self.members):
                if member.id == father_id:
                    father_idx = index
                if member.id == mother_id:
                    mother_idx = index
            #print(f"found origin - father:{father_idx}, mother:{mother_idx}")

            father_weight = self.members[father_idx].model.get_layer("dense1").get_weights()[0]
            mother_weight = self.members[mother_idx].model.get_layer("dense1").get_weights()[0]

            son_weight = mix_5050(father_weight, mother_weight)

            father_bias = self.members[father_idx].model.get_layer("dense1").get_weights()[1]
            mother_bias = self.members[mother_idx].model.get_layer("dense1").get_weights()[1]

            #TODO: maybe later we will need bias numbers
            #son_bias = mix_5050(father_bias, mother_bias)
            son_bias = father_bias

            son_dna = np.array([son_weight, son_bias], dtype=object)

            self.add_member_from_dna(son_dna)


def mix_5050(A, B):
    #print(f"A=")
    #for layer in A:
    #    print(layer)
    #print(f"B=")
    #for layer in B:
    #    print(layer)

    first = True
    result = None
    for i, layer in enumerate(A):
        mix_layer = []
        for j, cell in enumerate(layer):
            if randint(0,100) > 50: #50/50 method
                mix_layer.append(A[i][j])
            else:
                mix_layer.append(B[i][j])
        if first:
            result = np.array([mix_layer])
            first = False
        else:
            result = np.append(result, [mix_layer], axis=0)

    #print(f"R=")
    #for layer in result:
    #    print(layer)

    return result

            

    #model.get_layer(<<layer_name>>).get_weights()[0] # weights
    #model.get_layer(<<layer_name>>).get_weights()[1] # bias

    #model.layers[i].set_weights(listOfNumpyArrays)    
    #model.get_layer(layerName).set_weights(...)
    #model.set_weights(listOfNumpyArrays)