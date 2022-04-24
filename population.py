import logging
from random import randint, random
from dna import Dna
import numpy as np
import time
import logging
#from multiprocessing.pool import ThreadPool

class Population:
    def __init__(self, size):
        self.next_id = 0
        self.members = []
        for _ in range(size):
            self.add_random_member()

    def update_fitness(self):
        #pool = ThreadPool(processes=1)
        #threads = []
        
        start = time.time()
        for member in self.members:
            logging.debug(f"Testing DNA #{member.id}")
            #threads.append(pool.apply_async(member.test_dna_to_update_fitness))
            member.test_dna_to_update_fitness()
        #for t in threads:
        #    t.get()
        end = time.time()
        logging.debug(f"Time elapsed:{end - start}")

    def add_random_member(self):
        self.members.append(Dna(self.next_id))
        #print(f"Adding member id:{self.next_id}")
        self.next_id = self.next_id + 1

    def add_member_from_dna(self, dna):
        member = Dna(self.next_id)
        #model.get_layer(layerName).set_weights(...)
        member.model.get_layer("dense1").set_weights(dna)
        self.members.append(member)
        #print(f"Adding member id:{self.next_id}")
        self.next_id = self.next_id + 1

    def fill_with_random_members(self, quantity):
        for _ in range(quantity):
            self.add_random_member()

    def kill_under_performants(self, percentage_to_kill):
        results = sorted([member.fitness for member in self.members], reverse=False)
        min_accepted_result = results[int(percentage_to_kill/100*len(results))]
        self.members = [member for member in self.members if member.fitness > min_accepted_result]

    def get_best_members_ids(self, quantity):
        #print([f"{member.id}/{member.fitness}" for member in self.members])
        best_members = sorted(self.members, key = lambda x: x.fitness, reverse = True)[:quantity]
        best_members_ids = [member.id for member in best_members]
        #print(f"the best: {best_members_ids}")
        return best_members_ids

    def crossover_and_mutate(self, parents_ids, quantity, mutation_rate):
        if len(parents_ids) == 0:
            raise "generaition quiality too poor"
        while len(self.members) <= quantity:
            #print(f"starting crossover")
            #Yes, father and mother could be the same
            father_id = parents_ids[randint(0,len(parents_ids)-1)]
            mother_id = parents_ids[randint(0,len(parents_ids)-1)]
            
            #print(f"found a match! father:{father_id}, mother:{mother_id}")

            father_idx = mother_idx = -1
            for index, member in enumerate(self.members):
                if member.id == father_id:
                    father_idx = index
                if member.id == mother_id:
                    mother_idx = index
                if father_idx != -1 and mother_idx != -1:
                    break
            #print(f"found origin - father:{father_idx}, mother:{mother_idx}")

            father_dna = self.members[father_idx].model.get_layer("dense1").get_weights()
            mother_dna = self.members[mother_idx].model.get_layer("dense1").get_weights()

            father_weight = father_dna[0]
            mother_weight = mother_dna[0]

            mutate = False
            #if randint(1,100) <= mutation_rate:
            #    mutate = True

            son_weight = mix_5050(father_weight, mother_weight, mutate)

            father_bias = father_dna[1]
            mother_bias = mother_dna[1]

            #TODO: maybe later we will need bias numbers
            #son_bias = mix_5050(father_bias, mother_bias)
            son_bias = father_bias
            
            print(f"father: {father_dna}")
            print(f"mother: {mother_dna}")
            print(f"son_weight: {son_weight}")
            print(f"son_bias: {son_bias}")

            son_dna = np.array([son_weight, son_bias], dtype=object)
            
            self.add_member_from_dna(son_dna)

def mix_5050(A, B, mutate):
    #print(f"A=")
    #for layer in A:
    #    print(layer)
    #print(f"B=")
    #for layer in B:
    #    print(layer)
    if mutate:
        if randint(1,2) == 1:
            #print(A)
            layers = len(A)
            #print(f"layers={layers}")
            mutant_layer = randint(1,layers)-1
            #print(f"mutant_layer={mutant_layer}")
            cells = len(A[mutant_layer])
            #print(f"cells={cells}")
            mutant_cell = randint(1,cells)-1
            #print(f"mutant_cell={mutant_cell}")
            #print(f"Mutant father {A[mutant_layer][mutant_cell]}")
            A[mutant_layer][mutant_cell] = (random()-0.5)*2
            #print(f"Mutant father {A[mutant_layer][mutant_cell]}")
        else:
            #print(B)
            layers = len(B)
            mutant_layer = randint(1,layers)-1
            cells = len(B[mutant_layer])
            mutant_cell = randint(1,cells)-1
            #print(f"Mutant mother {B[mutant_layer][mutant_cell]}")
            B[mutant_layer][mutant_cell] = (random()-0.5)*2
            #print(f"Mutant mother {B[mutant_layer][mutant_cell]}")

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