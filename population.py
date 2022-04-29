import logging
from random import randint, random
from dna import Dna
import numpy as np
import time
import logging
import json
import jsonpickle
from json import JSONEncoder
#from multiprocessing.pool import ThreadPool

#random.seed(0)

class Population:
    def __init__(self, size):
        self.next_id = 0
        self.members = []
        for _ in range(size):
            self.add_random_member()

    def save_best_to_file(self):
        #filename = time.strftime("winner-%Y%m%d-%H%M%S.json")
        filename = time.strftime("winner-%Y%m%d.json")
        best = -1
        best_fitness = 0
        for idx, member in enumerate(self.members):
            if member.fitness > best_fitness:
                best_fitness = member.fitness
                best = idx

        print("")
        print(f"Best so far: id[{self.members[best].id}] name[{self.members[best].name}] fitness[{self.members[best].fitness}]")
        print("")

        data = {}
        data['sizes'] = self.members[best].model.sizes
        data['biases'] = self.members[best].model.biases
        data['weights'] = self.members[best].model.weights

        json_data = jsonpickle.encode(data)

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)

    def update_fitness(self, iterations=1):
        #pool = ThreadPool(processes=1)
        #threads = []
        
        start = time.time()
        for member in self.members:
            logging.debug(f"Testing DNA #{member.id}")
            #threads.append(pool.apply_async(member.test_dna_to_update_fitness))
            member.iterate_to_update_fitness(iterations)
            print('.', end='', flush=True)
        #for t in threads:
        #    t.get()
        end = time.time()
        logging.debug(f"Time elapsed:{end - start}")
        print('|')

    def add_random_member(self):
        self.members.append(Dna(self.next_id))
        #print(f"Adding member id:{self.next_id}")
        self.next_id = self.next_id + 1

    def add_member_from_dna(self, weights, biases, father_name, mother_name, mutate):
        member = Dna(self.next_id)
        member.name = f"{father_name}.{mother_name}"
        if mutate:
            member.name = f"M({member.name})"
        #print_model_details(member.model)
        #print(f"param dna: {dna}")
        member.model.weights = weights
        member.model.biases = biases

        self.members.append(member)
        #print(f"Adding member id:{self.next_id}")
        self.next_id = self.next_id + 1

    def fill_with_random_members(self, quantity):
        for _ in range(quantity):
            self.add_random_member()

    def kill_under_performants(self, percentage_to_kill):
        #results = sorted([member.fitness for member in self.members], reverse=False)
        #min_accepted_result = results[int(percentage_to_kill/100*len(results))]

        kill_upto_index = int(len(self.members)*percentage_to_kill/100.0)
        #print(f"Killing in the name of: {kill_upto_index}/{len(self.members)}")
        self.members = [member for idx,member in enumerate(self.members) if idx >= kill_upto_index]

    def get_best_members_ids(self, quantity):
        #print([f"{member.id}/{member.fitness}" for member in self.members])
        best_members = sorted(self.members, key = lambda x: x.fitness, reverse = True)[:quantity]
        best_members_ids = [member.id for member in best_members]
        #print(f"the best: {best_members_ids}")
        return best_members_ids

    def select_random_parent(parents_ids):
        return parents_ids[randint(0,len(parents_ids)-1)]

    def select_proportional_by_fitness_parent(self, parents_ids):
        #print("######")
        #print(f"parents_ids:{parents_ids}")
        parents_dict = {}
        total_fitness = 0
        for member in self.members:
            if member.id in parents_ids:
                parents_dict[member.id] = member.fitness
                total_fitness = total_fitness + member.fitness

        #print(f"parents_dict:{parents_dict}")
        #print(f"total_fitness:{total_fitness}")

        random_fitness_wheel = randint(1,total_fitness-1)
        #print(f"random_fitness_wheel:{random_fitness_wheel}")
        delete_me = 0
        for selected_parent_id in parents_dict:
            random_fitness_wheel = random_fitness_wheel - parents_dict[selected_parent_id]
            #print(f"random_fitness_wheel:{random_fitness_wheel}")
            if random_fitness_wheel <= 0:
                #print(f"selected_parent_id:{selected_parent_id}")
                return selected_parent_id
            delete_me = selected_parent_id
        #TODO: delete this:
        print("We shouldn't be here")
        raise
        #return delete_me

    def crossover_and_mutate(self, parents_ids, quantity, mutation_rate):
        if len(parents_ids) == 0:
            raise "generation quality is too poor"
        while len(self.members) <= quantity:
            #Yes, father and mother could be the same
            father_id = self.select_proportional_by_fitness_parent(parents_ids)
            mother_id = self.select_proportional_by_fitness_parent(parents_ids)
            
            father_idx = mother_idx = -1
            for index, member in enumerate(self.members):
                if member.id == father_id:
                    father_idx = index
                if member.id == mother_id:
                    mother_idx = index
                if father_idx != -1 and mother_idx != -1:
                    break
            
            father_weight = self.members[father_idx].model.weights
            mother_weight = self.members[mother_idx].model.weights
            father_biases = self.members[father_idx].model.biases
            mother_biases = self.members[mother_idx].model.biases

            mutate = False
            if randint(1,100) <= mutation_rate:
                mutate = True

            son_weight = mix(father_weight, mother_weight, mutate)
            son_biases = mix(father_biases, mother_biases, mutate)
            
            self.add_member_from_dna(son_weight, son_biases, self.members[father_idx].name, self.members[mother_idx].name, mutate)


def mix(A,B, mutate=False):
    """
    mixes lists of np arrays A and B (of weights or biases)
    selecting items for each positions randomly
    creating list C with same quantity and array structures

    if mutate then select a single data of a single array to randomize
    """
    C = []
    for i, WoB in enumerate(A):
        new_WoB = []
        for j, row in enumerate(WoB):
            new_row = []
            for k in range(len(row)):
                if randint(1,2) == 1:
                    new_value = A[i][j][k]
                else:
                    new_value = B[i][j][k]
                new_row.append(new_value)
            new_WoB.append(new_row)
        C.append(np.array(new_WoB))

    if mutate:
        i = randint(0,len(C)-1)
        WoB = C[i]
        j = randint(0,len(WoB)-1)
        row = WoB[j]
        k = randint(0,len(row)-1)
        C[i][j][k] = (random()-0.5)*2

    return C

def print_model_details(model):
    for layer in model.layers:
        print(layer.name)
        print("Weights")
        print("Shape: ",layer.get_weights()[0].shape,'\n',layer.get_weights()[0])
        print("Bias")
        print("Shape: ",layer.get_weights()[1].shape,'\n',layer.get_weights()[1],'\n')


"""
name dinamics

M(M(1.2.5.13).8)
"""