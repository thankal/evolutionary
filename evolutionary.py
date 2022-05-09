from math import *
from random import randint

POPULATION_SIZE = 10
NUM_OF_ITERATIONS = 50

x1 = []
x2 = []
F = x1^2 + x2 # the problem function


# helper routine to generate random values in the range [-1024, 1023]
def genRandomValues():
    temp = [] # make a list that holds the random values

    for i in range (POPULATION_SIZE):
        temp[i] = randint(-1024, 1023)

    return temp


def calculate_fitness(F):
    fitness, total_fitness, mean_fitness = 0

    for i in range(POPULATION_SIZE):
        fitness[i] = x1^2 + x2





    fitness_stats = (fitness, total_fitness, mean_fitness)
    return fitness_stats

def init():
    # initial population
    x1 = genRandomValues()
    x2 = genRandomValues()

def calculate_minimum(F):
    minimum = 0







    return minimum

