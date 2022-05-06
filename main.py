import logging
import sys
import time
from os import mkdir

from population import Population
from member import Member
from settings import *

def main():
    stats = set_stats_globals()
    config_new_logger()

    logging.info(f"STARTING NEW RUN")

    population = Population(size=POPULATION_SIZE)  
    for gen in range(GENERATIONS):
        
        logging.info(f"Starting Generation #{gen}")
        logging.info(f"Population size: {len(population.members)}")
        
        logging.debug(f"Updating fitness for Generation #{gen}")
        start = time.time()
        population.update_fitness(iterations=ITERATIONS_PER_GENERATION)
        end = time.time()
        fitness_time = end - start
        logging.info(f"Updating fitness for Generation #{gen} - completed in {fitness_time}")

        stats['run']['gen'] = gen
        population.save_best_to_file(data=stats)

        results = [member.fitness for member in population.members]
        top_results = sorted(results)[-10:]
        logging.info(f"Top 10 results for Generation #{gen}:{top_results}")
        stats['results'][gen] = {}
        stats['results'][gen]['min'] = min(results)
        stats['results'][gen]['max'] = max(results)
        stats['results'][gen]['avg'] = sum(results)/len(results)
        stats['results'][gen]['avg_top_10'] = sum(top_results)/len(top_results)
        stats['results'][gen]['fitness_time'] = fitness_time

        logging.info(f"Stats for gen:{gen}, max:{stats['results'][gen]['max']}, avg:{stats['results'][gen]['avg']:2f}, avg top 10:{stats['results'][gen]['avg_top_10']:2f}, fitness time:{fitness_time}")
        
        new_population = Population(0)
        
        #TODO: change Dna name class to Member
        parents_dna: list[Member]
        parents_dna = population.best_members(TOP_PARENTS_SELECTED) #list of dna's
    
        if ADD_PARENTS:
            new_population.add_members(parents_dna)
            #TODO: is this the same? remove add_members_from_dna method
            #population.members = parents_dna
            logging.debug(f"Adding parents for Generation #{gen} - completed")
        
        if CROSSOVERS_TO_ADD > 0:
            logging.debug(f"Adding crossovers for Generation #{gen}")
            start = time.time()
            new_population.crossover_members(parents_dna, CROSSOVERS_TO_ADD, MUTATION_RATE, "perc", "random")
            end = time.time()
            logging.info(f"Adding crossovers for Generation #{gen} - completed in {end - start}")
        
        if RANDOM_MEMBERS_TO_ADD > 0:
            population.add_random_members(RANDOM_MEMBERS_TO_ADD)
            logging.info(f"Filling some random members for Generation #{gen} - completed")

        population=new_population    
    
def config_new_logger():
    global RUN_NAME
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s', 
                              '%m-%d-%Y %H:%M:%S')
    
    filename = time.strftime("run_details.log")
    file_handler = logging.FileHandler(RUN_NAME+"/"+filename, mode='w')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.DEBUG)
    stdout_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stdout_handler)


def set_stats_globals():

    global RUN_NAME
    RUN_NAME = time.strftime("%Y.%m.%d_%H.%M")

    mkdir(RUN_NAME)

    stats = {}
    stats['results'] = {}
    stats['run'] = {}
    stats['config'] = {
        'POPULATION_SIZE': POPULATION_SIZE, 
        'GENERATIONS': GENERATIONS, 
        'RANDOM_MEMBERS_TO_ADD': RANDOM_MEMBERS_TO_ADD, 
        'ITERATIONS_PER_GENERATION':ITERATIONS_PER_GENERATION, 
        'MUTATION_RATE':MUTATION_RATE, 
        'TOP_PARENTS_SELECTED':TOP_PARENTS_SELECTED, 
        'ADD_PARENTS':ADD_PARENTS, 
        'CROSSOVERS_TO_ADD':CROSSOVERS_TO_ADD,
        'NN_ARQ':NN_ARQ,
        'BOARD_SIZE':BOARD_SIZE,
        'MAX_STEPS_WITHOUT_FOOD':MAX_STEPS_WITHOUT_FOOD,
        'RUN_NAME':RUN_NAME,
        }
    return stats
    
if __name__ == '__main__':
    main()