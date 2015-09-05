__author__ = 'duc07'

import math
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt
import numpy as np

dic = {}


def draw_plot(X, Y, Z):
    # X = X.ravel()
    # Y = Y.ravel()
    # Z = Z.ravel()
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm,
            linewidth=0, antialiased=False)
    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
    fig.colorbar(surf, shrink=0.5, aspect=5)
    plt.show()


def draw_plot2(x, y, z):
    from mpl_toolkits.mplot3d import Axes3D
    from matplotlib import cm
    import matplotlib.pyplot as plt

    x = x.ravel()
    y = y.ravel()
    z = z.ravel()
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.plot_trisurf(x, y, z, cmap=cm.jet, linewidth=0.2)
    plt.show()


def gen_grid():
    X,Y = np.mgrid[0:1:0.01, 0:1:0.01]
    X,Y = np.where(X + Y <= 1, X, 0), np.where(X + Y <= 1, Y, 0)
    return X, Y


@np.vectorize
def calc_entropy(a, b):
    global dic
    k = str(a) + '-' + str(b)
    val = - a * log2(a) - b * log2(b) - (1 - a - b) * log2(1 - a - b)
    if k not in dic:
        dic[k] = [val]
    else:
        dic[k].append(val)
    # print 'value = ', 1 - a - b
    return val


def log2(a):
    return 0 if a <= 0 else math.log(a, 2)


def main():
    X, Y = gen_grid()
    # print X, Y
    Z = calc_entropy(X, Y)
    for k, v in dic.iteritems():
        print k, ' - ', v
    print 'X=', X.shape
    print 'X=', Y.shape
    print 'X=', Z.shape
    draw_plot(X, Y, Z)
    draw_plot2(X, Y, Z)


if __name__ == "__main__":
    main()
    # X, Y = np.mgrid[0:1:0.2, 0:1:0.2]
    # print X, '\n\n', Y, '\n\n'
    # X, Y = np.where(X + Y <= 1, X, 0), np.where(X + Y <= 1, Y, 0)
    # print X, '\n\n', Y
    # Z = calc_entropy(X, Y)
    # print '\n\n', Z
