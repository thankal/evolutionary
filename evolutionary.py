from audioop import add
from math import *
from random import *

POPULATION_SIZE = 10
NUM_OF_ITERATIONS = 50

CROSSOVER_PROBABILITY = 0.8
MUTATION_PROBABILITY = 0.2

x1 = []
x2 = []
F = [] # the problem function

r = 0 # the random pool index (keep track of what random value to fetch next)

# helper routine to generate random values in the range [-1024, 1023]
def initialize():
    # initial population
    global x1, x2
    x1 = genRandomValues()
    x2 = genRandomValues()


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
def genRandomValues():
    temp = [] # make a list that holds the random values

    for i in range (POPULATION_SIZE):
        temp[i] = randint(-1024, 1023)

    return temp


# calculate the input function and evaluate fitness values for a whole generation
def evaluate(F):
    fitness = []
    total_fitness, mean_fitness = 0

    for i in range(POPULATION_SIZE):
        F[i] = x1[i]^2 + x2[i]
        fitness[i] = F[i]
        total_fitness += fitness[i]

    mean_fitness = total_fitness / POPULATION_SIZE
    fitness_stats = (fitness, total_fitness, mean_fitness)
    return fitness_stats

def select(in_population, fitness, total_fitness):
    selection_probabilities = [] 
    additive_probabilities = [] 
    random_pool = generateRandomPool()
    out_population = [] # the output of the function

    # for every chromosome in the population, calculate their selection probabilities...
    for i in range(POPULATION_SIZE):
        selection_probabilities[i] = fitness[i]/total_fitness

        # ...and now calculate the additive probabilities
        additive_probabilities[i] += selection_probabilities[i]


    # now initiate the selection proccess
    for i in range(POPULATION_SIZE):
        for j in range(POPULATION_SIZE):
            if (getNextRandom() <= additive_probabilities[j]):
                out_population[i] = in_population[j] 

    # return the selected chromosomes
    return  out_population 

def mutate(in_population):
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
        if (getNextRandom() < MUTATION_PROBABILITY)
            # ..xor that mask with the chromosome so that it gets mutated 
            out_population[i] = in_population[i] ^ mask;

    # return the mutated population
    return  out_population 

# crossover chromosomes in pairs of two
def crossover(in_population):
    out_population = []

    # get pairs..
    for i in range(1, POPULATION_SIZE, 2):
        # ..and depending on the crossover probability..
        if (getNextRandom() < CROSSOVER_PROBABILITY):
            # ..find the crossover point
            crossover_point = getNextRandom()*10 # at what digit we take the crossover (e.g. 0.45 -> after 4th digit)

            # only change x1 value
            pad=0

            # only change x2 value
            if getNextRandom() >= 0.5 :
                pad=11 # a.k.a. begin from the 11th bit
            

            chromosome1 = in_population[i-1]
            chromosome2 = in_population[i]

            # ..and swap the bits between the chromosomes
            for int b in range(11):
                chromosome1[crossover_point]


    # return the modified population
    return out_population


# excecutes the evolutionary algorithm
def calculate_minimum(F):
    minimum = 0
    generation = []


    initialize() # create a starting population
    random_pool = generateRandomPool() # create the random number pool

    # evaluate the starting population
    fitness, total_fitness, mean_fitness = evaluate(F) 

    # runs for each evolution step
    for e in range(NUM_OF_ITERATIONS):
        





    return minimum





calculate_minimum(F) # run simulation