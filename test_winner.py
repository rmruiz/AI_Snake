from member import Member
from json import load
from jsonpickle import decode
from settings import *
                  
def run():

    filename = input("Ingrese nombre de archivo:")

    with open(filename, 'r', encoding='utf-8') as f:
        json_data = load(f)
    
    data = decode(json_data)
    member = Member(data['NeuralNetwork']['weights'],data['NeuralNetwork']['biases'])

    global BOARD_SIZE
    BOARD_SIZE = data['config']['BOARD_SIZE']
    print("SETTINGS:")
    print(F"RUN_NAME:{data['config']['RUN_NAME']}")
    print(F"POPULATION_SIZE:{data['config']['POPULATION_SIZE']}")
    print(F"RANDOM_MEMBERS_TO_ADD:{data['config']['RANDOM_MEMBERS_TO_ADD']}")
    print(F"ITERATIONS_PER_GENERATION:{data['config']['ITERATIONS_PER_GENERATION']}")
    print(F"MUTATION_RATE:{data['config']['MUTATION_RATE']}")
    print(F"TOP_PARENTS_SELECTED:{data['config']['TOP_PARENTS_SELECTED']}")
    print(F"ADD_PARENTS:{data['config']['ADD_PARENTS']}")
    print(F"CROSSOVERS_TO_ADD:{data['config']['CROSSOVERS_TO_ADD']}")
    print(F"BOARD_SIZE:{data['config']['BOARD_SIZE']}")
    print(F"MAX_STEPS_WITHOUT_FOOD:{data['config']['MAX_STEPS_WITHOUT_FOOD']}")
    print(F"RUN_NAME:{data['config']['RUN_NAME']}")
    print(F"NN_ARQ:{data['config']['NN_ARQ']}")

    start = input("Start?")
    if start == "N" or start == "n":
        exit()
    
    member.play_game_to_update_fitness(print_test=True)
    
    
if __name__ == '__main__':
    run()

        