import math


class Ant:
    def __init__(self, nodes, start, distance_callback, alpha, beta) -> None:
        self.start = start  # None by default

    def distance(self, c1, c2):
        dx = c1[0] - c2[0]
        dy = c1[1] - c2[1]
        dist = math.sqrt(dx**2 + dy**2)
        return dist

    def choose_next(self):
        pass


class AntColony:
    antArray = []

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

        # Create all ants
        for _ in range(ant_count):
            self.antArray.append(Ant(nodes, start, alpha, beta))
