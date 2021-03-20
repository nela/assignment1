import numpy as np
from scipy.optimize import linprog
from scipy.optimize import minimize
from scipy.ndimage.interpolation import shift
import random
# import generate_rt_prices
from objects import ElAppliance

# price = np.zeros(10)
#
# for i in range(len(price)):
#     price[i] = random.uniform(0.1, 0.5)

h = 24

np.random.seed(4)
pr = np.random.random(5)
print(pr)
c = np.append(pr, pr)

A_ub = np.array([
    [1, 0, 0, 0, 0],
    [0, 1, 0, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 0, 1, 0],
    [0, 0, 0, 0, 1]])

b_ub = np.array([0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0])
A_eq = np.array([[1, 1, 1, 1, 1]])
b_eq = 9.9


 # res = linprog(pr, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq)
 # print(res)
 # print(np.round_(res.x, decimals=2))
# ev = ElAppliance("Electric Vehicle", 9.9, 9.9, 3, timeMin=21, timeMax=8)
shifted = np.roll(b_ub, 1)
print(shifted)
m = np.subtract(b_ub, shifted)
print("hhhh")
print(m)
c = np.random.random(13)
print(c)

def objective(b_ub):
    shifted = np.roll(b_ub, 1)
    m = np.subtract(np.power(b_ub, 2), np.power(shifted, 2))
    return sum(np.multiply(c, b_ub)) + sum(m)


def make_bounds(b_ub):
    return [(0.0, b.astype('float')) for b in b_ub]

<<<<<<< HEAD
=======
# ineq
def constraint1(b_ub):
    return sum(b_ub) - 9

cons1 = {'type': 'eq', 'fun': constraint1}
constraints = [cons1]
sol = minimize(objective, b_ub, method="SLSQP", bounds=make_bounds(b_ub), constraints=constraints)
print(sol)
print(np.round_(sol.x, decimals=2))


>>>>>>> master
