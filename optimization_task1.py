import numpy as np
from scipy.optimize import linprog
from objects import ElAppliance, Household

ev = ElAppliance("Electric Vehicle", 3.3, 3.3, 3)
dw = ElAppliance("Dishwasher", 1.44, 1.44, 1)
lm = ElAppliance("Laundry Machine", 1.94, 1.94, 1)

house = Household("Mi Casa", [ev, dw, lm])

prices = np.zeros(24)

for i in range(len(prices)):
    prices[i] = 1 if 17 <= i <= 20 else 0.5

A_ub = []
H = 23

# print(house)
# print(house.elAppliance)
for a in house.elAppliance:
    a_ub = []

    for h in range(a.duration):
        a_ub.insert(h, 1)

    for h in range(a.duration, H + 1):
        a_ub.insert(h, 0)

    print(a_ub)






