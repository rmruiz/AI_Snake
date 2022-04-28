import logging
import sys
import time
import numpy as np
#import tensorflow as tf
#tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

from population import Population

POPULATION_SIZE = 2000#2000
GENERATIONS = 100
ITERATIONS_PER_GENERATION = 1
KEEP_X_PERC_BEST = 20 #20
RANDOM_MEMBERS_PER_GENERATION = 3
MUTATION_RATE = 2
TOP_PARENTS_SELECTED = 50 #100
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
        
        results = sorted([member.fitness for member in population.members], reverse=False)
        logging.info(results)

        stats['results'][gen] = {}
        stats['results'][gen]['min'] = min(results)
        stats['results'][gen]['max'] = max(results)
        stats['results'][gen]['avg'] = np.mean(results)
        stats['results'][gen]['stdev'] = np.std(results)

        print(f"{gen} {stats['results'][gen]['min']} {stats['results'][gen]['max']} {stats['results'][gen]['avg']} {stats['results'][gen]['stdev']}")

        #Selection
        population.kill_under_performants(100-KEEP_X_PERC_BEST)
        
        #crossover and mutation
        parents_ids = population.get_best_members_ids(TOP_PARENTS_SELECTED)
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