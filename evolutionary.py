from audioop import add
from math import *
from random import *

POPULATION_SIZE = 10
NUM_OF_ITERATIONS = 50

CROSSOVER_PROBABILITY = 0.8
MUTATION_PROBABILITY = 0.2

r = 0 # the random pool index (keep track of what random value to fetch next)

# helper routine to generate random values in the range [-1024, 1023]
def initialize():
    # initial population
    starting_population = []

    for i in range(POPULATION_SIZE):
        starting_population[i] = genRandomChromosome() # just a population of random chromosomes (starting values for variables x1, x2)

    return starting_population

# generate a random pool of numbers (20) in range [0, 1] for use later. 
def generateRandomPool():
    random_pool = []
    for i in range(20):
        random_pool[i] = uniform(0, 1)

    # return the random pool of real numbers 
    return random_pool

def getNextRandom(random_pool):
    global r
    # return the next random. If reached the end (20th random) then cycle back from the beginning
    return random_pool[r%20] 


# generate random values for the initial population
def genRandomChromosome():
    random_chromosome = bin(randint(-1024, 1023))[2:] # random integer in binary representation for variable x1
    random_chromosome += bin(randint(-1024, 1023))[2:] # same for x2

    return random_chromosome


# calculate the input function and evaluate fitness values for a whole generation
def evaluate(population):
    fitness = []
    total_fitness, mean_fitness = 0

    for i in range(POPULATION_SIZE):
        x1x2 = population[i] # inlcudes x1 bits with x2 bits (total 22 bits)
        x1 = int(x1x2[11:]) # first 11 bits -> to int
        x2 = int(x1x2[-11:]) # last 11 bits -> to int

        fitness[i] = x1^2 + x2
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
        selection_probabilities[i] = fitness[i]/total_fitness

        # ...and now calculate the additive probabilities
        additive_probabilities[i] += selection_probabilities[i]


    # now initiate the selection proccess
    for i in range(POPULATION_SIZE):
        for j in range(POPULATION_SIZE):
            if (getNextRandom(random_pool) <= additive_probabilities[j]):
                out_population[i] = in_population[j] 

    # return the selected chromosomes
    return  out_population 

def mutate(in_population, random_pool):
    out_population = []
    mask = "0b0000000000000000000000" # make a mask in order to change one bit of the chromosome (22 bits)

    # mutate one random bit from each chromosome of the population
    for i in range(POPULATION_SIZE):
        # generate a random mask
        for b in range(22):
            temp = str(random.randint(0, 1))
            if temp == 1: 
                mask += '0' * (22-i) # complete the bits (we only want one '1' bit)
            mask += temp
            
        # depending on the mutation probability..
        if (getNextRandom(random_pool) < MUTATION_PROBABILITY):
            # ..xor that mask with the chromosome so that it gets mutated 
            out_population[i] = in_population[i] ^ mask;

    # return the mutated population
    return  out_population 

# crossover chromosomes in pairs of two
def crossover(in_population, random_pool):
    out_population = []

    # get pairs..
    for i in range(1, POPULATION_SIZE, 2):
        # ..and depending on the crossover probability..
        if (getNextRandom(random_pool) < CROSSOVER_PROBABILITY):
            # ..find the crossover point
            crossover_point = getNextRandom(random_pool)*10 # at what digit we take the crossover (e.g. 0.45 -> after 4th digit)

            ## The chromosome includes the concatenation of two variables x1 and x2.
            ## We need one crossover point so either set the crossover point on x1 or x2
            ## If we included all the binary digits from the crossover point and after, the crossover would mess up the variable values completely; we do not want that

            # only change x1 value
            pad=0

            # only change x2 value
            if getNextRandom(random_pool) >= 0.5 :
                pad=11 # a.k.a. begin from the 11th bit
            

            # get the pair to initiate the crossover on
            chromosome1 = in_population[i-1]
            chromosome2 = in_population[i]

            temp = []
            # ..and swap the bits between the chromosomes
            for b in range(11-crossover_point): # only include one variable e.g. xxxxxx[xxxxx]|yyyyyyyyyyy - ([crossover_bits])
                chromosome1[pad+crossover_point] = temp[b]
                chromosome1[pad+crossover_point] = chromosome2[pad+crossover_point]
                chromosome2[pad+crossover_point] = temp[b]
        
            # save the changes to the output population
            out_population[i-1] = chromosome1
            out_population[i] = chromosome2


    # return the modified population
    return out_population


def printPopulation(population):
    temp =  ''
    for c in population:
        temp += f"{c}\n"
    return temp


# excecutes the evolutionary algorithm
def calculate_minimum():
    minimum = 0


    generation = initialize() # create a starting population
    random_pool = generateRandomPool() # create the random number pool

    # evaluate the starting population

    # runs for each evolution step
    for e in range(NUM_OF_ITERATIONS):
        fitness, total_fitness, mean_fitness = evaluate(generation) 
        crossover(generation, random_pool)
        mutate(generation, random_pool)
        generation = select(generation, fitness, total_fitness, random_pool)

        printPopulation(generation)
        print('\n')

    return minimum





calculate_minimum(F) # run simulation