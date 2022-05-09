from math import *
from random import randint

POPULATION_SIZE = 10
NUM_OF_ITERATIONS = 50

x1 = []
x2 = []
F = [] # the problem function


# helper routine to generate random values in the range [-1024, 1023]
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

def select(parents, fitness, total_fitness):
    

    return offsprings


def initialize():
    # initial population
    global x1, x2
    x1 = genRandomValues()
    x2 = genRandomValues()

def calculate_minimum(F):
    minimum = 0
    generation = []

    initialize() # create a starting population

    # evaluate the starting population
    fitness, total_fitness, mean_fitness = evaluate(F) 

    # runs for each evolution step
    for e in range(NUM_OF_ITERATIONS):
        





    return minimum





calculate_minimum(F) # run simulation