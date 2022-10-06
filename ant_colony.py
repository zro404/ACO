import math
import random


class Ant:
    def __init__(self, nodes, pheromoneMap, start, alpha, beta) -> None:
        self.nodes = nodes
        self.pheromoneMap = pheromoneMap
        self.alpha = alpha
        self.beta = beta

        self.possible_nodes = []

        self.first_pass = True

        if start:
            self.currentNode = start
        else:
            self.currentNode = random.choice(nodes)

        self.choose_next(alpha, beta)

    def distance(self, c1, c2):
        dx = c1[0] - c2[0]
        dy = c1[1] - c2[1]
        dist = math.sqrt(dx**2 + dy**2)
        return dist

    def probablity(self, path, pheromone):
        pass

    def choose_next(self):
        most_probable = (None, 0)

        for path in self.pheromoneMap.keys():
            # check if path starts from current node
            if path[0] == self.currentNode:
                self.possible_nodes.append(path)

        # 50% probablity on first pass
        if self.first_pass:
            return random.choice(self.possible_nodes)

        for path in self.possible_nodes:
            p = self.probablity(path, self.nodes[path])

            if most_probable[1] < p:
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
