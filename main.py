from population import Population
from multiprocessing.pool import ThreadPool

POPULATION_SIZE = 50
GENERATIONS = 50

def main():
  #create population  
  population = Population(size=POPULATION_SIZE)  
  for _ in range(GENERATIONS):
    #print("#####################################")
     
    #print(population.members[0].get_weights())
    #print(population.members[0].get_next_move([0.5, 0.5, 0.5, 0.5]))

    pool = ThreadPool(processes=8)
    threads = []
    for member in population.members:
        #print(f"## TESTING DNA #{member.id} ##")
        #member.test_dna_to_update_fitness()
        threads.append(pool.apply_async(member.test_dna_to_update_fitness))
        
    for t in threads:
        t.get()
        
    #for member in population.members:
    #    print(f"Member ID:{member.id}, fitness:{member.fitness}")
    #test population (get fitness)
        #print fitness stats
    #selection & breeding (crossover)

    # kill 90% of under performant members
    results = sorted([member.fitness for member in population.members], reverse=False)
    min_accepted_result = results[int(0.9*len(results))]
    print(results)
    #print(min_accepted_result)

    population.members = [member for member in population.members if member.fitness > min_accepted_result]

    #for member in population.members:
    #    print(f"Member ID:{member.id}, fitness:{member.fitness}")

    fathers = [member.id for member in population.members]

    #print(f"{fathers=}")

    # duplicate members using crossover
    population.crossover_50_50(fathers, len(population.members), POPULATION_SIZE)
    # fill with random new members
    #print("creating random members")
    population.fill_with_random_members(POPULATION_SIZE)

    #for member in population.members:
    #    print(f"Member ID:{member.id}, fitness:{member.fitness}")

if __name__ == '__main__':
    main()