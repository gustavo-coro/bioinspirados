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

    
class AG:
    def __init__(self, graph:Graph, pop_size:int, 
                 generations:int, mutation_rate:float, crossover_rate:float, 
                 num_elite:int, crossover_type:int):
        self.graph = graph
        self.pop_size = pop_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.num_elite = num_elite
        self.crossover_type = crossover_type
        self.solutions = []
        
        for i in range(self.pop_size):
            sol = self.graph.random_solution()
            fit = self.graph.calculate_fitness(sol)
            idv = Individual(sol, fit)
            self.solutions.append(idv)

    def roulette_selection(self) -> list:
        total_fitness = 0
        for i in range(self.pop_size):
            total_fitness += self.solutions[i].fitness
        relative_fitness = []
        for i in range(self.pop_size):
            relative_fitness.append(self.solutions[i].fitness / total_fitness)
        cumulative_probability = [sum(relative_fitness[:i + 1]) for i in range(len(relative_fitness))]
        indices_populacao = list(range(self.pop_size))

        parents = []
        iterations = (self.pop_size - self.num_elite)
        if (iterations % 2 != 0):
            iterations += 1
        while len(parents) < iterations:
            rand = random.random()
            for i, cp in enumerate(cumulative_probability):
                if rand <= cp and indices_populacao[i] not in parents:
                    parents.append(indices_populacao[i])
                    break
                
        return [self.solutions[i] for i in parents]
    
    def tournament_selection(self) -> list:
        parents = []
        iterations = (self.pop_size - self.num_elite)
        if (iterations % 2 != 0):
            iterations += 1
        while len(parents) < iterations:
            vencedor = 0
            f_idv = random.randrange(0, self.pop_size)
            s_idv = random.randrange(0, self.pop_size)
            while(f_idv == s_idv):
                s_idv = random.randrange(0, self.pop_size)
            if(self.solutions[f_idv].fitness <= self.solutions[s_idv].fitness):
                vencedor = f_idv
            else:
                vencedor = s_idv
            parents.append(self.solutions[vencedor])

            f_idv = random.randrange(0, self.pop_size)
            while(f_idv == vencedor):
                f_idv = random.randrange(0, self.pop_size)
            s_idv = random.randrange(0, self.pop_size)
            while(s_idv == vencedor):
                s_idv = random.randrange(0, self.pop_size)
            while(f_idv == s_idv):
                s_idv = random.randrange(0, self.pop_size)
            if(self.solutions[f_idv].fitness <= self.solutions[s_idv].fitness):
                vencedor = f_idv
            else:
                vencedor = s_idv
            parents.append(self.solutions[vencedor])
        return parents

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

    def mutation(self, solutions:list):
        iterations = (self.pop_size - self.num_elite)
        if (iterations % 2 != 0):
            iterations += 1
        for i in range(iterations):
            for j in range(self.graph.num_cities): 
                r = npr.rand()
                if r < self.mutation_rate:
                    random_idx = npr.randint(low=0, high=self.graph.num_cities)
                    if (random_idx == j):
                        random_idx = npr.randint(low=0, high=self.graph.num_cities)
                    aux = solutions[i].solution[j]
                    solutions[i].solution[j] = solutions[i].solution[random_idx]
                    solutions[i].solution[random_idx] = aux

    def return_sorted_solutions(self) -> list:
        return sorted(self.solutions, key=lambda sol : sol.fitness)

    def run(self):
        best_solution = self.solutions[0]
        iteration = 0
        max_repeats = self.generations * 0.1
        iter_no_improvement = 0
        while((iteration < self.generations) and (iter_no_improvement < max_repeats)):
            parents = []
            if (self.crossover_type == 0):
                parents = self.roulette_selection()
            else:
                parents = self.tournament_selection()
            offspring = self.ox_crossover(parents)
            self.mutation(offspring)
            best = self.return_sorted_solutions()
            self.solutions = offspring
            for i in range(self.num_elite):
                self.solutions.append(best[i])

            if (best[0].fitness < best_solution.fitness):
                best_solution = best[0]
                iter_no_improvement = 0
            print(f"I = {iteration} | Melhor Fitness: {best_solution.fitness}") 
            iteration += 1
            iter_no_improvement += 1


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
pop_size = int(sys.argv[2])
generations = int(sys.argv[3])
num_elite = int(sys.argv[4])
crossover_rate = float(sys.argv[5])
mutation_rate = float(sys.argv[6])
crossover_type = int(sys.argv[7])
exit_file_path = sys.argv[8]

graph = create_graph_from_file(file_path)

ag = AG(graph=graph, pop_size=pop_size, 
        generations=generations, mutation_rate=mutation_rate,
          crossover_rate=crossover_rate, num_elite=num_elite, crossover_type=crossover_type)
ag.run()

best = ag.return_sorted_solutions()
print("Solução: ", best[0].solution)
print("Fitness: ", best[0].fitness)

with open(exit_file_path, 'a+') as file:
    file.write(f"{best[0].fitness}\n")
file.close()