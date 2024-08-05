import numpy as np
import numpy.random as npr
import random
import sys

class Graph:
    def __init__(self, num_cities:int, distances:list):
        self.num_cities = num_cities
        self.distances = distances

    def random_solution(self) -> list:
        # considering a complete graph
        arr = np.arange(self.num_cities)
        npr.shuffle(arr)
        return arr.tolist()
    
    def calculate_length(self, solution) -> int:
        length = 0
        for i in range(self.num_cities):
            length += self.distances[solution[i-1]][solution[i]]
        return length
    
class Individual:
    def __init__(self, solution:list, length:int):
        self.solution = solution
        self.length = length

    def has_edge(self, i:int, j:int) -> bool:
        index_i = self.solution.index(i)
        if (index_i == (len(self.solution) - 1)):
            if (self.solution[0] == j):
                return True
            else:
                return False
        elif (self.solution[index_i + 1] == j):
            return True
        else:
            return False

    
class AS:
    def __init__(self, graph:Graph, ant_pop_size:int, iterations:int, pheromone_quantity:float, pheromone_acceptance:float, distance_acceptance:float, evaporation_rate:float, q_constant:float, best_to_save:int):
        self.graph = graph
        self.ant_pop_size = ant_pop_size
        self.iterations = iterations
        self.pheromone_quantity = pheromone_quantity
        self.pheromone_acceptance = pheromone_acceptance
        self.distance_acceptance = distance_acceptance
        self.evaporation_rate = evaporation_rate
        self.q_constant = q_constant
        self.best_to_save = best_to_save
        self.ants = []
        self.best_ant = Individual(list(), float('inf'))

        self.pheromone_matrix = []
        for i in range(self.graph.num_cities):
            a = []
            a = a + [self.pheromone_quantity]*(graph.num_cities - len(a))
            self.pheromone_matrix.append(a)

        for i in range(self.ant_pop_size):
            solution = []
            solution.append(i)
            ant = Individual(solution, 0)
            self.ants.append(ant)

    def probabilistic_selection_function(self, i:int, remnant_cities:list):
        probabilities = []
        denominator = 0

        for j in remnant_cities:
            distance_ij = self.graph.distances[i][j]
            pheromone_ij = self.pheromone_matrix[i][j]
            denominator += (pow(pheromone_ij, self.pheromone_acceptance) * pow(distance_ij, self.distance_acceptance))
        
        for j in remnant_cities:
            distance_ij = self.graph.distances[i][j]
            pheromone_ij = self.pheromone_matrix[i][j]
            numerator = (pow(pheromone_ij, self.pheromone_acceptance) * pow(distance_ij, self.distance_acceptance))
            probability = numerator / denominator
            probabilities.append(probability)
        
        chosen_city = npr.choice(a=remnant_cities, p=probabilities)
        
        return chosen_city
    
    def pheromone_atualization(self, best_ants:list):
        for i in range(self.graph.num_cities):
            for j in range(self.graph.num_cities):
                self.pheromone_matrix[i][j] = (1 - self.evaporation_rate) * self.pheromone_matrix[i][j]
                sum = 0
                for k in range(self.best_to_save):
                    if (best_ants[k].has_edge(i, j)):
                        sum += ((self.best_to_save - k) * (self.q_constant / best_ants[k].length))
                self.pheromone_matrix[i][j] += sum

    def return_sorted_solutions(self) -> list:
        return sorted(self.ants, key=lambda ant : ant.length)
    
    def print_pheromone_matrix(self):
        for i in range(self.graph.num_cities):
            for j in range(self.graph.num_cities):
                print("{:.2f}".format(self.pheromone_matrix[i][j]), end="\t")
            print("")
        print("")

    def run(self):
        iteration = 0
        while (iteration < self.iterations):

            for k in range(self.ant_pop_size):
                start_city  = self.ants[k].solution[0]
                remnant_cities = [i for i in range(self.graph.num_cities)]
                remnant_cities.remove(start_city)
                self.ants[k].solution = []
                self.ants[k].solution.append(start_city)
                index = 0

                while(len(remnant_cities) > 0):
                    new_city = self.probabilistic_selection_function(self.ants[k].solution[index], remnant_cities)
                    self.ants[k].solution.append(new_city)
                    remnant_cities.remove(new_city)

                self.ants[k].length = self.graph.calculate_length(self.ants[k].solution)
                if (self.ants[k].length < self.best_ant.length):
                    self.best_ant.solution = self.ants[k].solution
                    self.best_ant.length = self.ants[k].length

            best_ants = self.return_sorted_solutions()
            best_ants = best_ants[:self.best_to_save]
            self.pheromone_atualization(best_ants)
            print(self.best_ant.length)

            iteration += 1


def create_graph_from_file(file_path) -> Graph:
    with open(file_path, 'r') as file:
        lines = file.readlines()
    file.close()

    adjacency_matrix = []
    for line in lines:
        row = [int(weight) for weight in line.split()]
        adjacency_matrix.append(row)

    num_nodes = len(adjacency_matrix)

    graph = Graph(distances=adjacency_matrix, num_cities=num_nodes)
    
    return graph




graph = create_graph_from_file("entradas/lau15_dist.txt")

ant_system = AS(graph, graph.num_cities, 500, pow(10, -6), 1.0, 5.0, 0.5, 100, 5)
ant_system.run()
print("Best = ", ant_system.best_ant.solution)
print("Length = ", ant_system.best_ant.length)