from ast import Str
import logging
from random import randint, random
from dna import Dna
import numpy as np
import time
import logging
import json
import jsonpickle
from snakegame import SnakeGame
from json import JSONEncoder
import copy

import multiprocessing
from joblib import Parallel, delayed

#from multiprocessing.pool import ThreadPool

#random.seed(0)

class Population:
    def __init__(self, size):
        self.next_id = size
        self.members = [Dna(i) for i in range(size)]

    def add_crossover_members_from_dna(self, parents_dna: list[Dna], quantity, mutation_rate:int, crossover_type, crossover_w_or_b):

        mutate: bool = mutation_rate > randint(1,100)
        new_dnas = []
        for _ in range(quantity):
            father_dna = new_select_proportional_by_fitness(parents_dna)
            #print(f"father_dna:{father_dna.model.weights}")
            mother_dna = new_select_proportional_by_fitness(parents_dna)
            #print(f"mother_dna:{mother_dna.model.weights}")

            new_dna = mix_dna(father_dna, mother_dna, mix_type=crossover_type, mix_weights_or_biases=crossover_w_or_b, mutate=mutate)
            #print(f"new_dna:{new_dna.model.weights}")
            new_dnas.append(new_dna)
        self.add_members_from_dna(new_dnas)

    def add_members_from_dna(self, list_of_dna: list[Dna]) -> None:
        for dna in list_of_dna:
            new_member = Dna(self.next_id, empty=True)
            self.next_id = self.next_id + 1
            new_member.model = dna.model
            self.members.append(new_member)

    def get_parents_dna(self, quantity:int) -> list[Dna]:
        return sorted(self.members, key = lambda x: x.fitness, reverse = True)[:quantity]

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
        #print(f"Best so far: id[{self.members[best].id}] name[{self.members[best].name}] fitness[{self.members[best].fitness}]")
        print(f"Best so far: id[{self.members[best].id}] fitness[{self.members[best].fitness}]")

        data = {}
        #data['sizes'] = self.members[best].model.sizes
        data['nn_architecture'] = self.members[best].model.nn_architecture
        data['biases'] = self.members[best].model.biases
        data['weights'] = self.members[best].model.weights

        json_data = jsonpickle.encode(data)

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)

    def update_fitness(self, iterations=1):
        #num_cores = multiprocessing.cpu_count()
        num_cores = 1 # use all of them
        start = time.time()
        results = Parallel(n_jobs=num_cores) ( delayed( new_iterate_to_update_fitness ) ( member, iterations ) for member in self.members )

        for i, member in enumerate(self.members):
            member.fitness = results[i]
        end = time.time()
        logging.debug(f"Time elapsed:{end - start}")

    def add_random_member(self):
        self.members.append(Dna(self.next_id))
        #print(f"Adding member id:{self.next_id}")
        self.next_id = self.next_id + 1

    def add_member_from_dna(self, weights, biases, father_name=None, mother_name=None, mutate=None):
        member = Dna(self.next_id)
        #member.name = f"{father_name}.{mother_name}"
        #if mutate:
        #    member.name = f"M({member.name})"
        #print_model_details(member.model)
        #print(f"param dna: {dna}")
        member.model.weights = weights
        member.model.biases = biases

        self.members.append(member)
        #print(f"Adding member id:{self.next_id}")
        self.next_id = self.next_id + 1

    def fill_with_random_members(self, quantity):
        self.members = self.members + [Dna(i) for i in range(self.next_id, self.next_id + quantity)]


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
            
            #self.add_member_from_dna(son_weight, son_biases, self.members[father_idx].name, self.members[mother_idx].name, mutate)
            self.add_member_from_dna(son_weight, son_biases)

def new_iterate_to_update_fitness(member, iterations=1) -> int:
    results = []
    for i in range(iterations):
        result = new_test_dna_to_update_fitness(member)
        results.append(result)
    return int(sum(results)/len(results))

def new_test_dna_to_update_fitness(member:Dna) -> int:
    sg = SnakeGame()
    while(sg.alive):
        input = sg.get_current_input()
        next_move = member.next_move_from_input(input)
        sg.move_snake(next_move)
    #print(".",end='',flush=True)
    return sg.get_fitness_score()

def mix_dna(dnaA: Dna,dnaB: Dna, mix_type:str="single", mix_weights_or_biases:str="random", mutate:bool=False):
    """
    mix_type=all (swap all randomly)
    mix_type=perc (swal perc% randomly)
    mix_type=single (swap one value randomly)

    mix_weights_or_biases=weights
    mix_weights_or_biases=biases
    mix_weights_or_biases=both
    mix_weights_or_biases=random
    """
    percentage_to_mix = 50
    i=0
    j=0
    k=0
    new_dna:Dna = Dna(0,empty=True)
    new_dna.model.weights = copy.deepcopy(dnaA.model.weights)
    new_dna.model.biases = copy.deepcopy(dnaA.model.biases)

    change_weights:bool = (mix_weights_or_biases == "random" and randint(0,1) == 0) or mix_weights_or_biases == "weights" or mix_weights_or_biases == "both"
    change_biases:bool = (mix_weights_or_biases == "random" and randint(0,1) == 1) or mix_weights_or_biases == "biases" or mix_weights_or_biases == "both"

    if mix_type == "all" or mix_type == "perc":
        if change_weights:
            for i, w in enumerate(dnaA.model.weights):
                for j, row in enumerate(w):
                    for k in range(len(row)):
                        if mix_type == all or percentage_to_mix > randint(1,100):
                            new_dna.model.weights[i][j][k] = dnaB.model.weights[i][j][k]
        if change_biases:
            for i, b in enumerate(dnaA.model.biases):
                for j, row in enumerate(b):
                    for k in range(len(row)):
                        if mix_type == all or percentage_to_mix > randint(1,100):
                            new_dna.model.biases[i][j][k] = dnaB.model.biases[i][j][k]
    else: #mix_type == "single"
        if change_weights:
            i = randint(0,len(new_dna.model.weights)-1)
            j = randint(0,len(new_dna.model.weights[i])-1)
            k = randint(0,len(new_dna.model.weights[i][j])-1)
            new_dna.model.weights[i][j][k] = dnaB.model.weights[i][j][k]
            #print(dnaA.model.weights[i][j][k])
            #print(dnaB.model.weights[i][j][k])
            #print(new_dna.model.weights[i][j][k])
        if change_biases:
            i = randint(0,len(new_dna.model.biases)-1)
            j = randint(0,len(new_dna.model.biases[i])-1)
            k = randint(0,len(new_dna.model.biases[i][j])-1)
            new_dna.model.biases[i][j][k] = dnaB.model.biases[i][j][k]
            #print(dnaA.model.biases[i][j][k])
            #print(dnaB.model.biases[i][j][k])
            #print(new_dna.model.biases[i][j][k])

    #print(f"switch in:[{i},{j},{k}]")
        
    if mutate:
        if change_weights:
            i = randint(0,len(new_dna.model.weights)-1)
            j = randint(0,len(new_dna.model.weights[i])-1)
            k = randint(0,len(new_dna.model.weights[i][j])-1)
            new_dna.model.weights[i][j][k] = (random()-0.5)*2
            #print(dnaA.model.weights[i][j][k])
            #print(dnaB.model.weights[i][j][k])
            #print(new_dna.model.weights[i][j][k])
        if change_biases:
            i = randint(0,len(new_dna.model.biases)-1)
            j = randint(0,len(new_dna.model.biases[i])-1)
            k = randint(0,len(new_dna.model.biases[i][j])-1)
            new_dna.model.biases[i][j][k] = (random()-0.5)*2
            #print(dnaA.model.biases[i][j][k])
            #print(dnaB.model.biases[i][j][k])
            #print(new_dna.model.biases[i][j][k])
    
        #print(f"mutate:{mutate} [{i},{j},{k}]")        

    return new_dna

def mix(A,B, mix_type="all", mix_weights_or_biases="both", mutate=False):

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

def new_select_proportional_by_fitness(parents_dna: list[Dna]):
    total_fitness = 0
    for dna in parents_dna:
        total_fitness = total_fitness + dna.fitness

    random_fitness_wheel = randint(1,total_fitness-1)
    for selected_dna in parents_dna:
        random_fitness_wheel = random_fitness_wheel - selected_dna.fitness
        if random_fitness_wheel <= 0:
            return selected_dna

