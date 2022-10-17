import math
import random

from threading import Thread


class Ant(Thread):
    def __init__(
        self,
        nodes,
        pheromoneMap,
        tmpPheromoneMap,
        first_pass,
        start,
        alpha,
        beta,
        pheromone_constant,
        pheromone_evaporation_rate,
        agent_index
    ):
        Thread.__init__(self)

        self.nodes = nodes
        self.pheromoneMap = pheromoneMap
        self.tmpPheromoneMap = tmpPheromoneMap
        self.alpha = alpha
        self.beta = beta
        self.pheromone_constant = pheromone_constant
        self.pheromone_evaporation_rate = pheromone_evaporation_rate
        self.initialNode = start
        self.agent_index = agent_index

        self.first_pass = first_pass

    def run(self):
        self.trip = []
        self.trip_distance = 0
        self.current_node = self.initialNode

        while True:
            next_path = self.choose_next()
            self.trip.append(next_path)
            self.trip_distance += self.distance(next_path)

            # print(f"agent {self.agent_index}: {next_path}")

            if next_path[0] == self.current_node:
                self.current_node = next_path[1]
            elif next_path[1] == self.current_node:
                self.current_node = next_path[0]


            print(self.trip)
            print()

            # trip completion condition
            if self.initialNode in self.trip[-1]:
                if len(self.trip) != 1:
                    self.pheromone_update()
                    return


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


        for path in self.pheromoneMap:
            # check if path starts from current node

            if self.current_node not in path:
                continue

            if (path not in self.trip):
                # if (self.initialNode in path) and ((len(self.trip)+1) == len(self.nodes)):
                possible_nodes.append(path)

                # print(path)
                        


        

        # 50% probablity on first pass
        if self.first_pass:
            choice = random.choice(possible_nodes)
            return choice

        for i in range(len(possible_nodes)):
            path = possible_nodes[i]

            pheromone = self.pheromoneMap[path]

            # calculate weightage of path
            weightage = (pheromone**self.alpha) * (
                self.distance(path) ** self.beta
            )


            weightage_array.append(weightage)


        weightage_sum = sum(weightage_array)

        for i in range(len(possible_nodes)):
            path = possible_nodes[i]
            weightage = weightage_array[i]

            p = weightage / weightage_sum

            if p > most_probable[1]:
                most_probable = (path, p)

        return most_probable[0]

    def pheromone_update(self):
        for path in self.trip:

            pheromone = self.pheromoneMap[path]

            self.tmpPheromoneMap[path] = (
                1 - self.pheromone_evaporation_rate
            ) * pheromone 


            self.tmpPheromoneMap[path] += (self.pheromone_constant / self.trip_distance)

        # if self.first_pass:
        #     print(len(self.tmpPheromoneMap))

class AntColony:
    antArray = []
    pheromoneMap = {}
    tmpPheromoneMap = {}

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
    ):

        self.nodes = nodes
        self.pheromone_evaporation_rate = pheromone_evaporation_rate
        self.pheromone_constant = pheromone_constant
        self.iterations = iterations
        self.alpha = alpha
        self.beta = beta
        self.first_pass = True
        self.ant_count = ant_count

        if start:
            self.start = start
        else:
            self.start = random.choice(nodes)

        # Initialize Pheromone map
        self.init_pheromone_map()

        for iter in range(self.iterations):
            print("iteration: ", iter+1)

            # Create all ants
            for i in range(self.ant_count):
                if not self.first_pass:
                    self.antArray.pop(i)
                ant = self.init_ant(i)
                self.antArray.append(ant)
                ant.start()


            for ant in self.antArray:
                ant.join()

            for path in self.pheromoneMap:
                self.pheromoneMap[path] = self.tmpPheromoneMap[path]


            if self.first_pass:
                self.first_pass = False


    def init_ant(self, agent_index):
            return Ant(
                self.nodes,
                self.pheromoneMap,
                self.tmpPheromoneMap,
                self.first_pass,
                self.start,
                self.alpha,
                self.beta,
                self.pheromone_constant,
                self.pheromone_evaporation_rate,
                agent_index
            )


    def init_pheromone_map(self):
        all_paths = []
        for i in self.nodes:
            for j in self.nodes:
                if i is j:
                    continue
                elif ((i,j) in all_paths) or ((j, i) in all_paths):
                    continue

                all_paths.append((i,j))

                self.pheromoneMap[(i, j)] = 0
                self.tmpPheromoneMap[(i, j)] = 0

    def create_optimal_path(self):
        optimal_path = []

        current_node = self.start

        for _ in range(len(self.nodes)):
            best_path = ((None, None), 0)
            for path in self.pheromoneMap:
                if path[0] == current_node:
                    pheromone = self.pheromoneMap[path]
                    if pheromone > best_path[1]:
                        best_path = (path, pheromone)

            optimal_path.append(best_path[0])
            current_node = best_path[0][1]

        # return optimal_path
        return self.antArray[0].trip
