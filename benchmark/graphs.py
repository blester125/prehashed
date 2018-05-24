import math
import numpy as np
import matplotlib.pyplot as plt

def collision_prob(k, N):
    return 1 - (math.exp((-k * k * (k - 1))/(2 * N)))

def approx_prob(k, N):
    return (k * (k - 1)) / (2 * N)

def collisions():
    num_hashes = 2 ** 160
    x = [i for i in range(num_hashes)]
    y = [approx(i, num_hashes) for i in x]
    plt.plot(x, y)
    plt.show()

def approx_table():
    print(approx_prob(1.71e15, 2 ** 160))
    print(approx_prob(1.71e19, 2 ** 160))
    print(approx_prob(1.71e21, 2 ** 160))
    print(approx_prob(1.71e23, 2 ** 160))
    print(approx_prob(1.42e24, 2 ** 160))

if __name__ == "__main__":
    approx_table()
