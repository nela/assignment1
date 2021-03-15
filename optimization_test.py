import numpy as np
from scipy.optimize import linprog
import random
# import generate_rt_prices
from objects import ElAppliance

# price = np.zeros(10)
#
# for i in range(len(price)):
#     price[i] = random.uniform(0.1, 0.5)

h = 24

np.random.seed(4)
pr = np.random.random(10)
print(pr)
c = np.append(pr, pr)

A_ineq = np.array([
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1]])

b_ineq = np.array([3, 3, 3, 3, 3, 3, 3, 3, 3, 3])
A_eq = np.array([[1, 1, 1, 1, 1, 1, 1, 1, 1, 1]])
b_eq = 9.9

bounds = []
for i in range(len(A_ineq)):
    bounds.append((0.9, 3))

print(bounds)
print(len(bounds))

res = linprog(pr, A_ub=A_ineq, b_ub=b_ineq, A_eq=A_eq, b_eq=b_eq, bounds=bounds)
print(res)
# ev = ElAppliance("Electric Vehicle", 9.9, 9.9, 3, timeMin=21, timeMax=8)

