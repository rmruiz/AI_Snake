import logging
import sys
import time
from os import mkdir

from population import Population
from dna import Dna
from settings import *

def main():
    stats = set_stats_globals()
    config_new_logger()

    logging.info(f"STARTING NEW RUN")

    population = Population(size=POPULATION_SIZE)  
    for gen in range(GENERATIONS):
        print("")
        print(f"Starting Generation #{gen}")
        print(f"Population size: {len(population.members)}")
        
        print(f"Updating fitness for Generation #{gen}")
        start = time.time()
        population.update_fitness(iterations=ITERATIONS_PER_GENERATION)
        end = time.time()
        logging.debug(f"Time elapsed:{end - start}")
        print(f"Updating fitness for Generation #{gen} - completed in {end - start}")
        
        if 'run' not in stats:
            stats['run'] = {}
        stats['run']['gen'] = gen
        population.save_best_to_file(data=stats)

        results = [member.fitness for member in population.members]
        top_results = sorted(results)[-10:]
        print(f"Results for Generation #{gen}:{top_results}")
        
        new_population = Population(0)
        
        #TODO: change Dna name class to Member
        parents_dna: list[Dna]
        parents_dna = population.get_best_members(TOP_PARENTS_SELECTED) #list of dna's
    
        if ADD_PARENTS:
            print(f"Adding parents for Generation #{gen}")
            new_population.add_members_from_dna(parents_dna)
            #TODO: is this the same? remove add_members_from_dna method
            #population.members = parents_dna
            print(f"Adding parents for Generation #{gen} - completed")
        
        #add CROSSOVERS_TO_ADD crossing 1 weight or 1 biases
        """
        crossover_type=all (swap all randomly)
        crossover_type=perc (swal perc% randomly) (fixed in 50%)
        crossover_type=single (swap one value randomly)

        crossover_w_or_b=weights
        crossover_w_or_b=biases
        crossover_w_or_b=both
        crossover_w_or_b=random
        """
        print(f"Adding crossovers for Generation #{gen}")
        new_population.add_crossover_members_from_dna(parents_dna, CROSSOVERS_TO_ADD, MUTATION_RATE, "single", "random")
        print(f"Adding crossovers for Generation #{gen} - completed")
        #   for each crossovers add both or only ADD_CROSSOVER_WINNER
        # fill with RANDOM_MEMBERS_TO_ADD
        if RANDOM_MEMBERS_TO_ADD > 0:
            print(f"Filling some random members for Generation #{gen}")
            population.fill_with_random_members(RANDOM_MEMBERS_TO_ADD)
            print(f"Filling some random members for Generation #{gen} - completed")

        population=new_population
        
        
    #logging.info(stats)
    #for gen in stats['results']: 
    #    logging.info(f"{gen} {stats['results'][gen]['min']} {stats['results'][gen]['max']} {stats['results'][gen]['avg']} {stats['results'][gen]['stdev']}")

    
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