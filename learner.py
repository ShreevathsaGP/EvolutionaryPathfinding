# learner.py

import sys
import math
import random
from globy import *

# dna
class DNA:
    length = 500 # [ no frames ]
    def __init__(self, points = None):
        if points:
            self.points = points # [ accelerations ]
            return
        # [ -1 <= acceleration < 1 ]
        self.points = [Vector(random.random() * 2 - 1, random.random() * 2 - 1) for _ in range(self.length)]

    def crossover(self, father):
        new_points = []
        mid = math.floor(random.randrange(self.length))
        for i in range(self.length):
            if i < mid:
                new_points.append(father.points[i])
            else:
                new_points.append(self.points[i])

        return DNA(new_points)

# gene pool
class GenePool:
    population_size = 2000
    def __init__(self):
        # population
        self.population = []
        self.gene_pool = []
        self.successful = []

        # fitness
        self.total_fitness = 0
        self.average_fitness = 0
        self.fittest_index = 0

        # time bound
        self.fastest_index = None
        self.fastest_time = None
        self.no_generations = 0

    def set_population(self, arrows):
        self.population = arrows

    def natural_selection(self):
        # population
        self.successful = []
        self.gene_pool = []

        # fitness
        self.total_fitness = 0
        self.average_fitness = 0
        self.fittest_index = 0

        # time bound
        self.fastest_time = None
        self.fastest_index = None
        
        # analyze population
        for i, arrow in enumerate(self.population):
            fitness = arrow.fitness()
            self.total_fitness += fitness
            if fitness > self.population[self.fittest_index].fitness():
                self.fittest_index = i

            if arrow.reached:
                self.successful.append(i)

                if arrow.time_taken:
                    if not self.fastest_time:
                        self.fastest_time = arrow.time_taken
                        self.fastest_index = i
                    else:
                        if arrow.time_taken < self.fastest_time:
                            self.fastest_time = arrow.time_taken
                            self.fastest_index = i

        self.average_fitness = self.total_fitness / len(self.population)
    
        # survival of the fittest
        for i, arrow in enumerate(self.population):
            fitness = arrow.fitness()
            size = int((fitness ** 2) * 100)
            if i == self.fittest_index  and len(self.successful) < 2:
                size = int((fitness ** 2) * 150)

            if i == self.fastest_index and len(self.successful) < 1:
                size = int((fitness ** 2) * 800)

            for _ in range(size):
                self.gene_pool.append(arrow.dna)

        # reproduction 
        for i, arrow in enumerate(self.population):
            m_index, f_index = random.randint(0, len(self.gene_pool) - 1), random.randint(0, len(self.gene_pool) - 1)
            mother_dna = self.gene_pool[m_index]
            father_dna = self.gene_pool[f_index]
            child_dna = mother_dna.crossover(father_dna)
            arrow.dna = child_dna

        self.no_generations += 1

        # print("----------------------------------------")
        # print("Average Fitness:", self.average_fitness)
        # print("Successful Arrows:", len(self.successful))
        # print("Fastest Time:", self.fastest_time)
        # print("----------------------------------------")
