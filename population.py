from time import strftime
from json import dump
from jsonpickle import encode
from copy import deepcopy
from random import randint, random
from joblib import Parallel, delayed

from member import Member
from settings import *

class Population:
    __slots__ = "members"
    def __init__(self, size):
        self.members = [Member() for _ in range(size)]

    def crossover_members(self, members: list[Member], quantity, mutation_rate:int, crossover_type, crossover_w_or_b):
        mutate: bool = mutation_rate > randint(1,100)
        new_members = []
        for _ in range(quantity):
            father = select_proportional_by_fitness(members)
            mother = select_proportional_by_fitness(members)
            new_member = cross_members(father, mother, mix_type=crossover_type, mix_weights_or_biases=crossover_w_or_b, mutate=mutate)
            new_members.append(new_member)
        self.add_members(new_members)

    def add_members(self, members: list[Member]) -> None:
        for member in members:
            weights = deepcopy(member.weights)
            biases = deepcopy(member.biases)
            self.members.append(Member(weights=weights, biases=biases))

    def add_random_members(self, quantity):
        self.members = self.members + [Member() for _ in range(quantity)]

    def best_members(self, quantity:int) -> list[Member]:
        return sorted(self.members, key = lambda x: x.fitness, reverse = True)[:quantity]

    def save_best_to_file(self, data):
        best_idx = -1
        best_fitness = 0
        for idx, member in enumerate(self.members):
            if member.fitness > best_fitness:
                best_fitness = member.fitness
                best_idx = idx

        best_fitness = self.members[best_idx].fitness

        dir_name = data['config']['RUN_NAME']
        filename = dir_name + "/" + strftime(f"{best_fitness}-%Y%m%d.json")

        data['NeuralNetwork'] = {}
        data['NeuralNetwork']['nn_architecture'] = self.members[best_idx].nn_architecture
        data['NeuralNetwork']['biases'] = self.members[best_idx].biases
        data['NeuralNetwork']['weights'] = self.members[best_idx].weights

        json_data = encode(data)

        with open(filename, 'w', encoding='utf-8') as f:
            dump(json_data, f, ensure_ascii=False, indent=4)

    def update_fitness(self, iterations=1):
        num_cores = -1 # use all of them
        results = Parallel(n_jobs=num_cores) ( delayed( p_iterate_to_update_fitness ) (member, iterations ) for member in self.members )
        for i, member in enumerate(self.members):
            member.fitness = results[i]
             
def p_iterate_to_update_fitness(member, iterations=1) -> int:
    return member.iterate_to_update_fitness(iterations)

def cross_members(mem1: Member,mem2: Member, mix_type:str="single", mix_weights_or_biases:str="random", mutate:bool=False):
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
    new_mem:Member = Member(weights=deepcopy(mem1.weights), biases=deepcopy(mem1.biases))

    change_weights:bool = (mix_weights_or_biases == "random" and randint(0,1) == 0) or mix_weights_or_biases == "weights" or mix_weights_or_biases == "both"
    change_biases:bool = (mix_weights_or_biases == "random" and randint(0,1) == 1) or mix_weights_or_biases == "biases" or mix_weights_or_biases == "both"

    if mix_type == "all" or mix_type == "perc":
        if change_weights:
            for i, w in enumerate(mem1.weights):
                for j, row in enumerate(w):
                    for k in range(len(row)):
                        if mix_type == all or percentage_to_mix > randint(1,100):
                            new_mem.weights[i][j][k] = mem2.weights[i][j][k]
        if change_biases:
            for i, b in enumerate(mem1.biases):
                for j, row in enumerate(b):
                    for k in range(len(row)):
                        if mix_type == all or percentage_to_mix > randint(1,100):
                            new_mem.biases[i][j][k] = mem2.biases[i][j][k]
    else: #mix_type == "single"
        if change_weights:
            i = randint(0,len(new_mem.weights)-1)
            j = randint(0,len(new_mem.weights[i])-1)
            k = randint(0,len(new_mem.weights[i][j])-1)
            new_mem.weights[i][j][k] = mem2.weights[i][j][k]
        if change_biases:
            i = randint(0,len(new_mem.biases)-1)
            j = randint(0,len(new_mem.biases[i])-1)
            k = randint(0,len(new_mem.biases[i][j])-1)
            new_mem.biases[i][j][k] = mem2.biases[i][j][k]
        
    if mutate:
        if change_weights:
            i = randint(0,len(new_mem.weights)-1)
            j = randint(0,len(new_mem.weights[i])-1)
            k = randint(0,len(new_mem.weights[i][j])-1)
            new_mem.weights[i][j][k] = (random()-0.5)*2
        if change_biases:
            i = randint(0,len(new_mem.biases)-1)
            j = randint(0,len(new_mem.biases[i])-1)
            k = randint(0,len(new_mem.biases[i][j])-1)
            new_mem.biases[i][j][k] = (random()-0.5)*2     

    return new_mem

def select_proportional_by_fitness(members: list[Member]):
    total_fitness = 0
    for member in members:
        total_fitness = total_fitness + member.fitness

    random_fitness_wheel = randint(1,total_fitness-1)
    for selected_member in members:
        random_fitness_wheel = random_fitness_wheel - selected_member.fitness
        if random_fitness_wheel <= 0:
            return selected_member

