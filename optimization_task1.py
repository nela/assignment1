import numpy as np
from scipy.optimize import linprog
from objects import ElAppliance, Household


# Create vectors and matrices that define equality constraints
def eq_constraints(house: Household, hours = 24):
    A_eq, b_eq = [], []
    index, appliance_index = 0, 1

    for a in house.elAppliance:
        a_eq = []

        if index > 0:
            for h in range(0, index):
                a_eq.insert(h, 0)

        for h in range(index, hours * appliance_index):
            a_eq.insert(h, 1)

        if appliance_index * hours < hours * len(house.elAppliance):
            for h in range(hours * appliance_index, hours * len(house.elAppliance)):
                a_eq.insert(h, 0)

        index = hours * appliance_index
        appliance_index += 1

        A_eq.append(a_eq)
        b_eq.append(a.dailyUsageMax)

    return A_eq, b_eq


# Create vectors and matrices that define the inequality constraints
def ub_constraints(house: Household, hours = 24):
    A_ub, b_ub = [], []
    index, appliance_index = 0, 1

    for a in house.elAppliance:

        for rows in range(hours):
            a_ub = []

            if index > 0:
                for h in range(0, index):
                    a_ub.insert(h, 0)

            a_ub.insert(index, 1)
            index += 1

            for h in range(index, hours * len(house.elAppliance)):
                a_ub.insert(h, 0)

            A_ub.append(a_ub)
            b_ub.append(round(a.dailyUsageMax / float(a.duration), 3))

        index = hours * appliance_index
        appliance_index += 1

    return A_ub, b_ub


ev = ElAppliance("Electric Vehicle", 9.9, 9.9, 3, timeMin=0, timeMax=8)
lm = ElAppliance("Laundry Machine", 1.94, 1.94, 4, timeMin=8, timeMax=17)
dw = ElAppliance("Dishwasher", 1.44, 1.44, 1)

house = Household("Mi Casa", [ev, lm, dw])

A_eq, b_eq = eq_constraints(house)
A_ub, b_ub = ub_constraints(house)


prices = []
for i in range(24):
    prices.insert(i, 1) if 17 <= i <= 20 else prices.insert(i, 0.5)

cost_function_price_vector = []
for i in range(len(house.elAppliance)):
    cost_function_price_vector += prices

# print(len(prices))
# print(len(cost_function_price_vector))
# print(len(A_ub))
print(len(b_ub))
print(b_ub)
# print(len(A_eq))
# print(A_eq)
# print(len(b_eq))
# print(b_eq)
# print(A_eq)
# print(A_ub)
#
res = linprog(cost_function_price_vector,
        A_ub=A_ub, b_ub=b_ub,
        A_eq=A_eq, b_eq=b_eq)

print(res)
