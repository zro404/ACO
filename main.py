import matplotlib.pyplot as plt
import random
import math

from ant_colony import AntColony


plt.style.use("dark_background")


COORDS = (
    (20, 52),
    (43, 50),
    (20, 84),
    (70, 65),
    (29, 90),
    (87, 83),
    (73, 23),
)


def random_coord():
    r = random.randint(0, len(COORDS))
    return r


def distance(c1, c2):
    dx = c1[0] - c2[0]
    dy = c1[1] - c2[1]
    dist = math.sqrt(dx**2 + dy**2)
    return dist


def plot_nodes(w=12, h=8):
    for x, y in COORDS:
        plt.plot(x, y, "g.", markersize=15)
    plt.axis("off")
    fig = plt.gcf()
    fig.set_size_inches([w, h])


def plot_all_edges():
    paths = ((a, b) for a in COORDS for b in COORDS)

    for a, b in paths:
        plt.plot((a[0], b[0]), (a[1], b[1]))


plot_nodes()

colony = AntColony(COORDS, ant_count=1, iterations=1)

optimal_edges = colony.create_optimal_path()

for edge in optimal_edges:
    plt.plot((edge[0][0], edge[1][0]), (edge[0][1], edge[1][1]))
    pass


plt.show()
