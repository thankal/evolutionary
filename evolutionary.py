from audioop import add
from math import *
from msilib.schema import File
from random import *


POPULATION_SIZE = 6
NUM_OF_ITERATIONS = 10000
RANDOM_POOL_SIZE = 10

CROSSOVER_PROBABILITY = 0.3
MUTATION_PROBABILITY = 0.1

r = 0 # the random pool index (keep track of what random value to fetch next)

# helper routine to generate random values in the range [-1024, 1023]
def initialize():
    # initial population
    starting_population = []

    for i in range(POPULATION_SIZE):
        starting_population.append(genRandomChromosome()) # just a population of random chromosomes (starting values for variables x1, x2)

    return starting_population

# generate a random pool of numbers (20) in range [0, 1] for use later. 
def generateRandomPool():
    random_pool = []
    for i in range(40):
        random_pool.append(uniform(0, 1))

    # return the random pool of real numbers 
    return random_pool

def getNextRandom(random_pool):
    global r

    num = random_pool[r%RANDOM_POOL_SIZE]
    r+=1 # increment index

    # return the next random. If reached the end (20th random) then cycle back from the beginning
    return num


# generate random values for the initial population
def genRandomChromosome():
    random_chromosome = "{:011b}".format(randint(-1024, 1023)).replace("-", "1") # random integer in binary representation for variable x1
    random_chromosome += "{:011b}".format(randint(-1024, 1023)).replace("-", "1") # random integer in binary representation for variable x1

    return random_chromosome


# calculate the input function and evaluate fitness values for a whole generation
def evaluate(population):
    fitness = []
    total_fitness = mean_fitness = 0

    for i in range(POPULATION_SIZE):
        x1x2 = population[i] # inlcudes x1 bits with x2 bits (total 22 bits)
        part1 = x1x2[:11] # first 11 bits -> to int
        part2 = x1x2[11:] # last 11 bits -> to int

        if (part1[0] == '1'):
            x1 = int(('-' + part1[1:]), 2)
        else:
            x1 = int(part1, 2)

        if (part2[0] == '1'):
            x2 = int(('-' + part2[1:]), 2)
        else:
            x2 = int(part2, 2)


        fitness.append(pow(x1, 2)+x2) 
        total_fitness += fitness[i]

    mean_fitness = total_fitness / POPULATION_SIZE
    fitness_stats = (fitness, total_fitness, mean_fitness)
    return fitness_stats

def select(in_population, fitness, total_fitness, random_pool):
    selection_probabilities = [] 
    additive_probabilities = [] 
    out_population = [] # the output of the function

    # for every chromosome in the population, calculate their selection probabilities...
    for i in range(POPULATION_SIZE):
        selection_probabilities.append(fitness[i]/total_fitness) 
    # ...and now calculate the additive probabilities
    additive = 0
    for j in range(POPULATION_SIZE):
        additive += selection_probabilities[j]
        additive_probabilities.append(additive)



    # now initiate the selection proccess
    selected = 0
    i = 0
    while (selected < POPULATION_SIZE):
        # negate probabilities so that we favor minimums
        if (-(getNextRandom(random_pool)) <= -(selection_probabilities[i%POPULATION_SIZE])):
            out_population.append(in_population[i%POPULATION_SIZE]) # cycle through all candidate parents
            selected += 1
        i += 1

    # return the selected chromosomes
    return  out_population 

def mutate(in_population, random_pool):
    out_population = []

    # mutate one random bit from each chromosome of the population
    for i in range(POPULATION_SIZE):
        modified_chromosome = ''
        # now iterate through each chromosome of the population bit by bit
        for bit in in_population[i]:
            # depending on the mutation probability decide if we mutate each bit
            if (getNextRandom(random_pool) < MUTATION_PROBABILITY): 
                modified_chromosome += str(int(bit) ^ 1) # xor with 1 -> swap bit
            else:
                modified_chromosome += bit # keep bit unchanged

            
        # TODO: modifies next bit of what we said?

        out_population.append(modified_chromosome)

    # return the mutated population
    return  out_population 

# crossover chromosomes in pairs of two
def crossover(in_population, random_pool):
    out_population = []

    # get pairs..
    for i in range(1, POPULATION_SIZE, 2):
        # get the pair to initiate the crossover on
        chromosome1 = in_population[i-1]
        chromosome2 = in_population[i]

        # ..and depending on the crossover probability..
        if (getNextRandom(random_pool) < CROSSOVER_PROBABILITY):
            # ..find the crossover point
            crossover_point = int(getNextRandom(random_pool)*10) # at what digit we take the crossover (e.g. 0.45 -> after 4th digit)

            ## The chromosome includes the concatenation of two variables x1 and x2.
            ## We need one crossover point so either set the crossover point on x1 or x2
            ## If we included all the binary digits from the crossover point and after, the crossover would mess up the variable values completely; we do not want that

            # only change x1 value
            pad=0

            # only change x2 value
            if getNextRandom(random_pool) >= 0.5 :
                pad=10 # a.k.a. begin from the 11th bit
            


            # used for swapping operation
            temp1 = ''
            temp2 = '' 
            for b in range(11-crossover_point): # only include one variable e.g. xxxxxx[xxxxx]|yyyyyyyyyyy - ([crossover_bits])
                # save bits of each cromosome 
                temp1 += chromosome1[pad+crossover_point+b]
                temp2 += chromosome2[pad+crossover_point+b]

            # swap bits
            chromosome1 = chromosome1[:crossover_point] + temp2 + chromosome1[crossover_point+1+b:]
            chromosome2 = chromosome2[:crossover_point] + temp1 + chromosome2[crossover_point+1+b:]
        
        # save the changes to the output population
        out_population.append(chromosome1)
        out_population.append(chromosome2)


    # return the modified population
    return out_population


# format population for printing
def toStringPopulation(population, fitness):
    temp =  ''
    for i in range(POPULATION_SIZE):
        temp += f"{population[i]}"
        # convert chromosome to actual x1, x2 values for visualization purposes
        part1 = population[i][:11] # first 11 bits -> to int
        part2 = population[i][11:] # last 11 bits -> to int

        if (part1[0] == '1'):
            x1 = int(('-' + part1[1:]), 2)
        else:
            x1 = int(part1, 2)

        if (part2[0] == '1'):
            x2 = int(('-' + part2[1:]), 2)
        else:
            x2 = int(part2, 2)
        temp += '\t'
        temp += f"x1={x1}, x2={x2}"

        temp += f", fitness={fitness[i]}\n"
    return temp


# excecutes the evolutionary algorithm
def calculate_minimum():
    minimum = inf # keep track of the function's minimum 
    stats_string = ''
    stat_file = open("output.txt", 'w')

    generation = initialize() # create a starting population

    stats_string = f'-Starting population-\n'
    print(stats_string)
    stat_file.write(stats_string)


    random_pool = generateRandomPool() # create the random number pool


    # runs for each evolution step
    for step in range(NUM_OF_ITERATIONS):
        fitness, total_fitness, mean_fitness = evaluate(generation) 

        stats_string = f'Generation: {step}\n'
        stats_string += toStringPopulation(generation, fitness)
        stats_string += f'\nmean_fitness:{mean_fitness}, total_fitness:{total_fitness}'
        stats_string += '\n--------------------------\n'

        print(stats_string)
        stat_file.write(stats_string)

        if (mean_fitness < minimum): minimum = mean_fitness # update minimum

        # follow the process to create the next generation
        generation = crossover(generation, random_pool)
        generation = mutate(generation, random_pool)
        generation = select(generation, fitness, total_fitness, random_pool)



    stats_string += '\n==========================\n'
    print(stats_string)
    stat_file.write(stats_string)
    print(f'minimum mean value: {minimum}\n')
    stat_file.write(f'minimum mean fitness: {minimum}\n')
    stat_file.close()
    return minimum





calculate_minimum() # run simulation