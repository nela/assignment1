import numpy as np
from scipy.optimize import linprog
import random
import generate_rt_prices
# price = np.zeros(4)
#
# for i in range(len(price)):
#     price[i] = random.uniform(0.1, 0.5)

h = 24

np.random.seed(4)
pr = np.random.random(h)
print(pr)
c = np.append(pr, pr)

pr = generate_rt_prices.daily_price(0.2, 0.8)


dur = 4
it_number = h - dur # Duration


MA_ub = []
MA_eq = []

for i in range(it_number + 1):
    m = np.zeros([h, h])
    n = np.zeros(h)
    for j in range(dur):
        m[j+i][j+i] = 1
        n[j+i] = 1

    MA_eq.append(np.array([n]))
    MA_ub.append(np.squeeze(np.asarray(m)))

b_ub = np.full(h, 3)
b_eq = 9.9

all_prices = []

for i in range(len(MA_eq)):
    A_eq = MA_eq[i]
    A_ub = MA_ub[i]
    res = linprog(pr, A_ub, b_ub, A_eq, b_eq)
    values = res.x
    prv = np.dot(pr, values)
    all_prices.append(prv)

print(all_prices)

print(len(all_prices))



# A_ineq = np.array([
#     [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
#
# print(A_ineq)

#
# b_ineq = np.array([3, 3, 3, 3, 3, 1.5, 1.5, 1.5, 1.5, 1.5])
#
# A_eq = np.array([[1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 0, 1, 1, 1, 1, 0]])
#
# b_eq = np.array([9.9, 5.0])
#
# res = linprog(c, A_ub=A_ineq, b_ub=b_ineq, A_eq=A_eq, b_eq=b_eq)
# print(res)


