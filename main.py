import matplotlib.pyplot as plt
import numpy as np
import random
import math


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


def plot_coords(w=12, h=8):
    for x, y in COORDS:
        plt.plot(x, y, "g.", markersize=15)
    plt.axis("off")
    fig = plt.gcf()
    fig.set_size_inches([w, h])


def plot_all_paths():
    paths = ((a, b) for a in COORDS for b in COORDS)

    for a, b in paths:
        plt.plot((a[0], b[0]), (a[1], b[1]))


plot_coords()
plot_all_paths()
plt.show()
