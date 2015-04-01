__author__ = 'duc07'

import math
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt
import numpy as np


def draw_plot(X, Y, Z):
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm,
            linewidth=0, antialiased=False)
    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
    fig.colorbar(surf, shrink=0.5, aspect=5)
    plt.show()


def gen_grid():
    X,Y = np.mgrid[0:1:0.01, 0:1:0.01]
    X,Y = np.where(X + Y <= 1, X, 0), np.where(X + Y <= 1, Y, 0)
    return X, Y


@np.vectorize
def calc_entropy(a, b):
    return - a * log2(a) - b * log2(b) - (a + b) * log2(a + b)


def log2(a):
    return 0 if a == 0 else math.log(a, 2)


def main():
    X, Y = gen_grid()
    Z = calc_entropy(X, Y)
    draw_plot(X, Y, Z)


if __name__ == "__main__":
    main()


# age attr: 1 - [ 5/12 * (- 3/5 * log(2, 3/5) - 2/5 * log(2, 2/5))  + 5/12 * (- 2/5 * log(2, 2/5) - 3/5 * log(2, 3/5))  +  2/12 * (- 1/2 * log(2, 1/2) - 1/2 * log(2, 1/2))]

# breed atte: 1 - [ 3/12 * (-1/3 * log(2, 1/3) - 2/3 * log(2, 2/3)) + 2/12 * (0) + 3/12 * (-3/3 * log(2, 3/3) - 0) + 4/12 * (-2/4 * log(2, 2/4) - 2/4 * log(2, 2/4)) ]