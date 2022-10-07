import math
import random

from threading import Thread


class Ant(Thread):
    def __init__(self, nodes, pheromoneMap, start, alpha, beta) -> None:
        self.nodes = nodes
        self.pheromoneMap = pheromoneMap
        self.alpha = alpha
        self.beta = beta

        self.trip = []

        self.first_pass = True

        if start:
            self.trip[0] = start
        else:
            self.trip[0] = random.choice(nodes)

    def run(self):
        while True:
            next_path = self.choose_next()
            self.trip.append(next_path[1])

            # trip completion condition
            if self.trip[-1] == self.trip[0]:
                break

    def distance(self, path):
        (c1, c2) = path
        dx = c1[0] - c2[0]
        dy = c1[1] - c2[1]
        dist = math.sqrt(dx**2 + dy**2)
        return dist

    def choose_next(self):
        possible_nodes = []
        weightage_array = []

        most_probable = ((), 0)

        for path, pheromone in self.pheromoneMap:
            # check if path starts from current node
            if path[0] == self.trip[-1]:
                possible_nodes.append(path)

                # calculate weightage of path
                weightage = (pheromone**self.alpha) * (
                    self.distance(path) ** self.beta
                )
                weightage_array.append(path)

        weightage_sum = sum(weightage_array)

        # 50% probablity on first pass
        if self.first_pass:
            return random.choice(possible_nodes)

        for path, weightage in zip(possible_nodes, weightage_array):
            p = weightage / (weightage_sum - weightage)

            if p > most_probable[1]:
                most_probable = (path, p)

        return most_probable[0]


class AntColony:
    antArray = []
    pheromoneMap = {}

    def __init__(
        self,
        nodes,
        start=None,
        ant_count=50,
        alpha=0.5,
        beta=1.2,
        pheromone_evaporation_rate=0.40,
        pheromone_constant=1000.0,
        iterations=80,
    ) -> None:

        self.nodes = nodes
        self.pheromone_evaporation_rate = pheromone_evaporation_rate
        self.pheromone_constant = pheromone_constant

        # Initialize Pheromone map
        self.init_pheromone_map()

        # Create all ants
        for _ in range(ant_count):
            self.antArray.append(Ant(self.nodes, self.pheromoneMap, start, alpha, beta))

    def init_pheromone_map(self):
        for i in self.nodes:
            for j in self.nodes:
                if i is j:
                    continue

                self.pheromoneMap[(i, j)] = 0
