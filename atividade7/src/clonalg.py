import numpy as np
import numpy.random as npr
import random
import sys
import copy

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

    
class CLONALG:
    def __init__(self, graph:Graph, pop_size:int, generations:int, 
                 selection_area:int, quantity_change:int, cloning_factor:float):
        self.graph = graph
        self.pop_size = pop_size
        self.generations = generations
        self.selection_area = selection_area
        self.quantity_change = quantity_change
        self.cloning_factor = cloning_factor
        self.alfa = 0.03
        self.solutions = sorted(self.generate_initial_set(), key= lambda s: s.fitness)

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
            distances = self.get_distances_from_cities_in_lrc(last_city, lrc)

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
    
    def generate_initial_set(self) -> list:
        initial_set = list()
        while(len(initial_set) < self.pop_size):
            idv = self.random_greedy_solution()
            initial_set.append(idv)

        return initial_set

    def cloning(self, solutions: list) -> list:
        clones = []
        num_clones = []

        for i in range(self.selection_area):
            num_clones.append(round(self.cloning_factor * self.pop_size / (i+1)))

        for i in range(self.selection_area):
            for _ in range(num_clones[i]):
                clones.append(copy.deepcopy(solutions[i]))

        return clones


    def hypermutation(self, clones:list) -> list:
        iterations = len(clones)
        rho = 2

        fitness_array = np.array([f.fitness for f in clones])
        min_fitness = np.min(fitness_array)
        max_fitness = np.max(fitness_array)
        
        if min_fitness == max_fitness:
            normalized_fitness_array = np.ones_like(fitness_array)
        else:
            normalized_fitness_array = (fitness_array - min_fitness) / (max_fitness - min_fitness)


        mutation_rate = np.exp(-rho * normalized_fitness_array)

        for i in range(iterations):
            current_solution = clones[i].solution

            for _ in range(int(self.graph.num_cities * mutation_rate[i])):
                idx1, idx2 = npr.choice(range(self.graph.num_cities), size=2, replace=False)

                if idx1 > idx2:
                    idx1, idx2 = idx2, idx1
                
                current_solution[idx1:idx2 + 1] = reversed(current_solution[idx1:idx2 + 1])

            clones[i].solution = current_solution

        return clones

    def return_sorted_solutions(self) -> list:
        return sorted(self.solutions, key=lambda sol : sol.fitness)
    
    def diversity_control(self):
        self.solutions.sort(key=lambda s: s.fitness)

        for idx in range(self.pop_size - self.quantity_change, self.pop_size):
            self.solutions[idx] = self.random_greedy_solution()

    def run(self):
        iter = 0

        while iter < self.generations:
            print(f"Best fitness at iteration {iter}: {self.solutions[0].fitness}")

            selected_solutions = self.solutions[:self.selection_area]

            clones = self.cloning(selected_solutions)

            clones = self.hypermutation(clones)

            clones.sort(key=lambda s: s.fitness)

            new_sol = [clones[i] for i in range(self.selection_area)]
            self.solutions.extend(new_sol)

            self.solutions.sort(key=lambda s: s.fitness)
            self.solutions = self.solutions[:self.pop_size]

            self.diversity_control()

            self.solutions.sort(key=lambda s: s.fitness)

            iter += 1



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

file_path = sys.argv[1]
graph = create_graph_from_file(file_path)

clonalg = CLONALG(graph=graph, pop_size=20, generations=100, selection_area=8, quantity_change=8, cloning_factor=0.5)
clonalg.run()

best = clonalg.return_sorted_solutions()
print("Solução: ", best[0].solution)
print("Fitness: ", best[0].fitness)