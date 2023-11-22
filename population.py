from time import strftime
from json import dump
from jsonpickle import encode
from copy import deepcopy
from random import randint, random
from joblib import Parallel, delayed

from member import Member
from settings import *

DEFAULT_ITERATIONS = 100
class Population:
    __slots__ = "members", "iterations"
    def __init__(self, size=0, iterations=DEFAULT_ITERATIONS):
        self.members = [Member() for _ in range(size)]
        #TODO: iterations should be inside Memmber
        self.iterations = iterations

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

    def print_stats(self, logging, gen):
        all_results = []
        all_results = self.get_results()
        mm = max(all_results)
        avg = sum(all_results)/len(all_results)
        top_results = sorted(all_results)[-10:]
        print(f"Top Results:{top_results}")
        avg_top_10 = sum(top_results)/10.0
        logging.info(f"Stats for gen:{gen}, max:{mm}, avg:{avg:2f}, avg top 10:{avg_top_10:2f}")
        return

    def save_best_to_file(self, data):

        #TODO: redo this

        #results: list[Member]
        #results = population.get_results()
        #top_results = sorted(results)[-10:]
        #logging.info(f"Top 10 results for Generation #{gen}:{top_results}")
        #stats['results'][gen] = {}
        #stats['results'][gen]['min'] = min(results)
        #stats['results'][gen]['max'] = max(results)
        #stats['results'][gen]['avg'] = sum(results)/len(results)
        
        #stats['results'][gen]['avg_top_10'] = sum(top_results)/len(top_results)
        #stats['results'][gen]['fitness_time'] = fitness_time

        #best_idx = -1
        #best_fitness = 0
        #for idx, member in enumerate(self.members):
        #    if member.fitness > best_fitness:
        #        best_fitness = member.fitness
        #        best_idx = idx

        #best_fitness = self.members[best_idx].fitness

        #dir_name = data['config']['RUN_NAME']
        #gen_num = data['run']['gen']
        #filename = f'{dir_name}/{gen_num:04}-' + strftime(f"{best_fitness:012}-%Y.%m.%d_%H.%M.%S.json")

        #data['NeuralNetwork'] = {}
        #data['NeuralNetwork']['nn_architecture'] = self.members[best_idx].nn_architecture
        #data['NeuralNetwork']['biases'] = self.members[best_idx].biases
        #data['NeuralNetwork']['weights'] = self.members[best_idx].weights

        #json_data = encode(data)

        #with open(filename, 'w', encoding='utf-8') as f:
        #    dump(json_data, f, ensure_ascii=False, indent=4)
        return

    def update_fitness(self):
        num_cores = PARALLEL_CPU
        results = Parallel(n_jobs=num_cores) ( delayed( p_iterate_to_update_fitness ) (member, self.iterations ) for member in self.members )
        #NOTETOSELF: Usando Parallel los objetos no son modificados, es necesario retornar el fitness
        for i, member in enumerate(self.members):
            member.fitness = results[i]
        
        #print(f"parallel iteration results:{results}")
        #print(f"update_fitness results:{[member.fitness for member in self.members]}")
             
    def get_results(self):
        return [member.fitness for member in self.members]

# Parallel needs method with parametes (not class methods)
def p_iterate_to_update_fitness(member, iterations=1):
    return member.iterate_to_update_fitness(iterations=iterations)

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
    #print("select_proportional_by_fitness")
    total_fitness = 0
    for member in members:
        total_fitness = total_fitness + member.fitness
        #print(f"total_fitness={total_fitness}")

    random_fitness_wheel = randint(0, total_fitness)
    for selected_member in members:
        random_fitness_wheel = random_fitness_wheel - selected_member.fitness
        if random_fitness_wheel <= 0:
            return selected_member

