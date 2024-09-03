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
    
    def calculate_fitness(self, solution) -> int:
        fitness = 0
        for i in range(self.num_cities):
            fitness += self.distances[solution[i-1]][solution[i]]
        return fitness
    
class Individual:
    def __init__(self, solution:list, fitness:int):
        self.solution = solution
        self.fitness = fitness

    
class SS:
    def __init__(self, graph:Graph, s:int, b1:int, b2:int, alfa:float):
        self.graph = graph
        self.s = s
        self.b1 = b1
        self.b2 = b2
        self.b = b1 + b2
        self.alfa = alfa
        self.initial_set = []
        self.ref_set = []

    def get_distances_from_cities_in_lrc(self, last_city, lrc):
        return [self.graph.distances[last_city][city] for city in lrc]

    def get_cities_lesser_than_limit(self, distances, lrc, limit):
        return [lrc[i] for i in range(len(lrc)) if distances[i] <= limit]

    def random_greedy_solution(self) -> Individual:
        initial_city = random.randint(0, self.graph.num_cities - 1)
        sol = [initial_city]

        lrc = list(range(self.graph.num_cities))
        lrc.remove(initial_city)

        while len(sol) < self.graph.num_cities:
            last_city = sol[-1]
            distances = self.get_distances_from_cities_in_lrc(last_city, self.graph.distances, lrc)

            min_distance = min(distances)
            max_distance = max(distances)
            limit = min_distance + self.alfa * (max_distance - min_distance)

            cities = self.get_cities_lesser_than_limit(distances, lrc, limit)
            
            if cities:
                next_city = cities[random.randint(0, len(cities) - 1)]
            else:
                next_city = lrc[random.randint(0, len(lrc) - 1)]

            sol.append(next_city)
            lrc.remove(next_city)
        
        s = Individual(sol, self.graph.calculate_fitness(sol))

        return s
    
    def generate_neighbor_2_opt(self, solucao:list, i:int, j:int):
        vizinho = solucao[:]
        vizinho[i:j] = reversed(vizinho[i:j])
        return vizinho

    def local_search(self, sol:Individual) -> Individual:
        s = Individual(sol.solution, sol.fitness)
        improv = True
        while(improv):
            neighbor = Individual(s.solution, s.fitness)
            for i in range(1, self.graph.num_cities - 1):
                for j in range(i + 1, self.graph.num_cities):
                    temp_sol = self.generate_neighbor_2_opt(neighbor.solution, i, j)
                    temp_distance = self.graph.calculate_fitness(temp_sol)

                    if (temp_distance < neighbor.fitness):
                        neighbor.solution = temp_sol
                        neighbor.fitness = temp_distance

            if (neighbor.fitness < s.fitness):
                s.solution = neighbor.solution
                s.fitness = neighbor.fitness
            else:
                improv = False

        return s

    
    def ref_set_update(self) -> list:
        # code
        print("")

    def ox_crossover(self, parents:list) -> list:
        offspring = list()
        offspring_number = 0
        iterations = (self.pop_size - self.num_elite)
        if (iterations % 2 != 0):
            iterations += 1
        while (offspring_number < iterations):
            r = npr.rand()
            if (r > self.crossover_rate):
                offspring.append(parents[offspring_number])
                offspring.append(parents[offspring_number + 1])
                offspring_number = offspring_number + 2
                continue

            f_parent = parents[offspring_number].solution
            s_parent = parents[offspring_number + 1].solution

            f_child = [-1] * self.graph.num_cities
            s_child = [-1] * self.graph.num_cities

            f_point = random.randint(0, self.graph.num_cities - 1)
            s_point = random.randint(f_point, self.graph.num_cities - 1)
            for i in range(f_point, s_point):
                f_child[i] = f_parent[i]
                s_child[i] = s_parent[i]

            remaining_positions = [i for i in range(self.graph.num_cities) if i not in range(f_point, s_point)]

            s_parent_index = 0
            for i in remaining_positions:
                while s_parent[s_parent_index] in f_child:
                    s_parent_index = (s_parent_index + 1) % self.graph.num_cities
                f_child[i] = s_parent[s_parent_index]
                s_parent_index = (s_parent_index + 1) % self.graph.num_cities

            offspring.append(Individual(f_child, self.graph.calculate_fitness(f_child)))

            f_parent_index = 0
            for i in remaining_positions:
                while f_parent[f_parent_index] in s_child:
                    f_parent_index = (f_parent_index + 1) % self.graph.num_cities
                s_child[i] = f_parent[f_parent_index]
                f_parent_index = (f_parent_index + 1) % self.graph.num_cities

            offspring.append(Individual(s_child, self.graph.calculate_fitness(s_child)))

            offspring_number = offspring_number + 2

        return offspring

    def return_sorted_solutions(self) -> list:
        return sorted(self.solutions, key=lambda sol : sol.fitness)

    def run(self):

        
        return self.ref_set



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

if __name__ == "__main__":

    file_path = sys.argv[1]

    graph = create_graph_from_file(file_path)