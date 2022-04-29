import logging
import sys
import time
import numpy as np

from population import Population

POPULATION_SIZE = 2000#2000
GENERATIONS = 50
ITERATIONS_PER_GENERATION = 1
KEEP_X_PERC_BEST = 20 #20
RANDOM_MEMBERS_PER_GENERATION = 30
MUTATION_RATE = 5
TOP_PARENTS_SELECTED = 100 #100
#CROSS_OVER = POPULATION_SIZE*KEEP_X_PERC_BEST-RANDOM_MEMBERS_PER_GENERATION

def main():
    stats = {}
    stats['config'] = {}
    stats['config']['POPULATION_SIZE'] = POPULATION_SIZE
    stats['config']['GENERATIONS'] = GENERATIONS
    stats['config']['KEEP_X_PERC_BEST'] = KEEP_X_PERC_BEST
    stats['config']['RANDOM_MEMBERS_PER_GENERATION'] = RANDOM_MEMBERS_PER_GENERATION
    stats['results'] = {}
    config_new_logger()

    logging.info(f"STARTING NEW RUN")

    population = Population(size=POPULATION_SIZE)  
    for gen in range(GENERATIONS):
        print(f"{gen}", end='', flush=True)
        
        population.update_fitness(iterations=ITERATIONS_PER_GENERATION)
        
        #Selection
        #print(f"population complete: {len(population.members)} members")
        population.kill_under_performants(100-KEEP_X_PERC_BEST)
        #print(f"population alive: {len(population.members)} sourvivours")

        results = [member.fitness for member in population.members]
        logging.info(results)
        #print(f"{gen} {min(results)} {max(results)} {np.mean(results)} {np.std(results)}")

        #print(f"{[member.name for member in population.members]}")
        
        #crossover and mutation
        parents_ids = population.get_best_members_ids(TOP_PARENTS_SELECTED)
        #print(f"PARENTS (TOP#{TOP_PARENTS_SELECTED})")
        #for i,member in enumerate(population.members):
        #    if member.id in parents_ids:
        #        print(f"idx[{i}] id[{member.id}] name[{member.name}] fitness[{member.fitness}]")
        #print(f"THE REST")
        #for i,member in enumerate(population.members):
        #    if member.id not in parents_ids:
        #        print(f"idx[{i}] id[{member.id}] name[{member.name}] fitness[{member.fitness}]")

        population.crossover_and_mutate(parents_ids, POPULATION_SIZE-RANDOM_MEMBERS_PER_GENERATION-1, MUTATION_RATE)
        
        population.fill_with_random_members(RANDOM_MEMBERS_PER_GENERATION)

        population.save_best_to_file()
        
    logging.info(stats)
    for gen in stats['results']: 
        logging.info(f"{gen} {stats['results'][gen]['min']} {stats['results'][gen]['max']} {stats['results'][gen]['avg']} {stats['results'][gen]['stdev']}")

    
def config_new_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s', 
                              '%m-%d-%Y %H:%M:%S')
    
    filename = time.strftime("%Y%m%d-%H%M%S.log")
    file_handler = logging.FileHandler("logs/"+filename, mode='w')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.DEBUG)
    stdout_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stdout_handler)


if __name__ == '__main__':
    main()


    """
    usar funcion max(lista, key=fuct) """