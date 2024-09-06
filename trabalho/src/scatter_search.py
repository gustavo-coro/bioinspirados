import numpy as np
import numpy.random as npr
import random
import itertools
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

    def __eq__(self, other): 
        if not isinstance(other, Individual):
            return NotImplemented

        return [a == b for a, b in zip(self.solution, other.solution)] and self.fitness == other.fitness

    
class SS:
    def __init__(self, graph:Graph, s:int, b1:int, b2:int, alfa:float):
        self.graph = graph
        self.s = s
        self.b1 = b1
        self.b2 = b2
        self.b = b1 + b2
        self.alfa = alfa
        self.initial_set = self.generate_initial_set()
        self.ref_set = self.ref_set_create()

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
    
    def generate_initial_set(self) -> list:
        initial_set = list()
        while(len(initial_set) < self.s):
            idv = self.random_greedy_solution()
            initial_set.append(self.local_search(idv))
        
        return initial_set
    
    def num_differing_edges(self, tour1:list, tour2:list) -> int:
        n = len(tour1)

        edges_tour1 = {(tour1[i], tour1[(i + 1) % n]) for i in range(n)}
        edges_tour2 = {(tour2[i], tour2[(i + 1) % n]) for i in range(n)}

        differing_edges = edges_tour1.symmetric_difference(edges_tour2)

        return len(differing_edges) // 2

    
    def ref_set_create(self) -> list:
        self.initial_set.sort(key=lambda x: (x.fitness))

        ref_set = self.initial_set[:self.b1]
        del self.initial_set[:self.b1]

        while (len(ref_set) < self.b):
            idx_most_dif_edges = 0
            most_dif_edges = 0
            
            for i in range(len(self.initial_set)):
                for sol in ref_set:
                    dif_edges = self.num_differing_edges(self.initial_set[i].solution, sol.solution)

                    if (dif_edges > most_dif_edges):
                        most_dif_edges = dif_edges
                        idx_most_dif_edges = i

            ref_set.append(self.initial_set[idx_most_dif_edges])
            self.initial_set.remove(self.initial_set[idx_most_dif_edges])

        return ref_set 

    def generate_subsets(self) -> list:
        sub_sets = list(itertools.combinations(self.ref_set, 2))
        
        return sub_sets

    def ox(self, sub_sets:list) -> list:
        solutions = list()

        for pair in sub_sets:
            f_solution = pair[0].solution
            s_solution = pair[1].solution

            f_new_solution = [-1] * self.graph.num_cities
            s_new_solution = [-1] * self.graph.num_cities

            f_point = random.randint(0, self.graph.num_cities - 1)
            s_point = random.randint(f_point, self.graph.num_cities - 1)
            for i in range(f_point, s_point):
                f_new_solution[i] = f_solution[i]
                s_new_solution[i] = s_solution[i]

            remaining_positions = [i for i in range(self.graph.num_cities) if i not in range(f_point, s_point)]

            s_solution_index = 0
            for i in remaining_positions:
                while s_solution[s_solution_index] in f_new_solution:
                    s_solution_index = (s_solution_index + 1) % self.graph.num_cities
                f_new_solution[i] = s_solution[s_solution_index]
                s_solution_index = (s_solution_index + 1) % self.graph.num_cities

            solutions.append(Individual(f_new_solution, self.graph.calculate_fitness(f_new_solution)))

            f_solution_index = 0
            for i in remaining_positions:
                while f_solution[f_solution_index] in s_new_solution:
                    f_solution_index = (f_solution_index + 1) % self.graph.num_cities
                s_new_solution[i] = f_solution[f_solution_index]
                f_solution_index = (f_solution_index + 1) % self.graph.num_cities

            solutions.append(Individual(s_new_solution, self.graph.calculate_fitness(s_new_solution)))

        return solutions

    def run(self):
        new_solutions = True

        while(new_solutions):
            print(self.ref_set[0].fitness)

            sub_sets = self.generate_subsets()
            solutions = self.ox(sub_sets)

            for i, s in enumerate(solutions):
                solutions[i] = self.local_search(s)

            solutions.extend(self.ref_set)

            unique_solutions = []
            seen_solutions = set()

            for s in solutions:
                solution_tuple = tuple(s.solution)
                if solution_tuple not in seen_solutions:
                    unique_solutions.append(s)
                    seen_solutions.add(solution_tuple)

            unique_solutions.sort(key=lambda x: x.fitness)
            unique_solutions = unique_solutions[:self.b]

            new_solutions = False

            for i in range(self.b):
                if (self.ref_set[i] != unique_solutions[i]):
                    new_solutions = True
                    break

            if (new_solutions):
                self.ref_set = unique_solutions
                
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

    ss = SS(graph=graph, s=40, b1=5, b2=5, alfa=0.03)

    ss.run()

    print("Melhor:")
    print(ss.ref_set[0].solution)
    print(ss.ref_set[0].fitness)