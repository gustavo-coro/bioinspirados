import random
import math

class RastriginFunction:
    def __init__(self, dimension):
        self.max_bound = 5.12
        self.min_bound = -5.12
        self.dimension = dimension

    def random_solution(self) -> list:
        return [random.uniform(self.min_bound, self.max_bound)
                for _ in range(self.dimension)]

    def evaluate_solution(self, x) -> float:
        d = self.dimension
        sum = 0
        for i in range(d):
            x_i = x[i]
            sum += (x_i ** 2) - (10 * math.cos(2 * math.pi * x_i))
        sum = 10 * self.dimension + sum
        return sum