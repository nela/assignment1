import numpy as np
import pandas as pd
from scipy.optimize import linprog
from objects import ElAppliance, Household, ElType

# Create vectors and matrices that define equality constraints
def create_eq_constraints(appliance: list, hours=24):
    A_eq, b_eq = [], []
    index = 0

    for a in appliance:
        a_eq = np.zeros(hours * len(appliance))

        for i in range(index + a.timeMin, index + a.timeMax):
            a_eq[i] = 1

        index += hours
        A_eq.append(a_eq)
        b_eq.append(a.dailyUsageMax)

    return A_eq, b_eq


# Create vectors and matrices that define the inequality constraints
def create_ub_constraints(appliances: list, hours=24):
    A_ub, b_ub = [], []
    index = 0

    for a in appliances:
        for h in range(hours):
            a_ub = np.zeros(hours * len(appliances))

            if h >= a.timeMin and h < a.timeMax:
                a_ub[index + h] = 1

            A_ub.append(a_ub)
            b_ub.append(a.maxHourConsumption)
        index += hours

    return A_ub, b_ub


def schedule_multiple_non_continuous_appliances(appliances: list,
        hourly_prices: list):
    c = []
    for i in range(len(appliances)):
        c += hourly_prices

    A_eq, b_eq = create_eq_constraints(appliances)
    A_ub, b_ub = create_ub_constraints(appliances)
    res = linprog(c, A_ub, b_ub, A_eq, b_eq)
    # print(res)
    x = np.round_(res.x, decimals=2)

    return [x[i:(i+24)] for i in range(0, len(x), 24)]


# hourly_prices = [0.1, 0.1,
#         0.3, 0.2, 0.1, 0.1, 0.2, 0.1, 0.3,
#         0.3, 0.3, 0.2,0.3, 0.3, 0.3, 0.2,0.3, 0.3, 0.3, 0.2,0.3, 0.3, 0.3, 0.1]


# lght = ElAppliance("Lighing", 1, 2, 0.2, 10, ElType.non_shiftable, timeMin=10, timeMax=20)
# heat = ElAppliance("Heating", 6.4, 9.6, 0.4, 24, ElType.non_shiftable, timeMin=0, timeMax=24)
# rfrg = ElAppliance("Refrigerator", 1.32, 3.96, 0.164, 24, ElType.non_shiftable, timeMin=0, timeMax=24)
# stove = ElAppliance("Stove", 3.9, 3.9, 2, 3, ElType.shiftable, timeMin=14, timeMax=22)
# tv = ElAppliance("Tv", 0.15, 0.6, 0.12, 5, ElType.non_shiftable, timeMin=17, timeMax=22)
# computer = ElAppliance("Computer", 0.6, 0.6, 0.1, 6, ElType.non_shiftable, timeMin=8, timeMax=24)
# router = ElAppliance("Router", 0.14, 0.14, 0.006, 24, ElType.non_shiftable, timeMin=0,timeMax=24)
# fan = ElAppliance("Ceiling Fan", 0.22, 0.22, 0.073, 3, ElType.shiftable_non_continious, timeMin=12, timeMax=20)
# freezer = ElAppliance("Freezer", 0.84, 0.84,  0.035, 24, ElType.non_shiftable, timeMin=0, timeMax=24)
# dw = ElAppliance("Dishwaasher", 1.44, 1.44, 1.44, 1, ElType.shiftable_non_continious, timeMin=14, timeMax=24)
# lm = ElAppliance("Laundry Machine", 1.94, 1.94, 0.485, 2, ElType.shiftable, timeMin=0, timeMax=18)
# dryer = ElAppliance("Cloth Dryer", 2.5, 2.5, 2.5, 1, ElType.shiftable, timeMin=0, timeMax=20)
# ev = ElAppliance("Electric batmobile", 9.9, 9.9, 3.3, 3, ElType.shiftable_non_continious, timeMin=0, timeMax=8)
# iron = ElAppliance("Cloth Iron", 0.28, 0.28, 0.28, 1, ElType.shiftable, timeMin=10, timeMax=20)
# cellcharger = ElAppliance("Cellphone charger", 0.01, 0.01, 0.003, 1, ElType.shiftable_non_continious, timeMin=0, timeMax=12)
# mw = ElAppliance("Microwave", 0.6, 0.6, 0.6, 1, ElType.shiftable, timeMin=17, timeMax=24)
# hd = ElAppliance("Hair Dryer", 0.19, 0.19, 0.19, 1, ElType.shiftable, timeMin=19, timeMax=23)
# toaster = ElAppliance("Toaster", 0.3, 0.3, 0.3, 1, ElType.shiftable, timeMin=12, timeMax=20)

# appliances = [lght, heat, rfrg, stove, tv, computer, router, fan, freezer,
#         dw, lm, dryer, ev, iron, cellcharger, mw, hd, toaster]
#
# appliances2 = [lght, heat]
# house = Household("Mi Casa", appliances)
#
# sch = schedule_multiple_non_continuous_appliances(appliances, hourly_prices)
# data = [list(x) for x in zip(*sch)]
# columns = [a.name for a in appliances]
# df = pd.DataFrame(data, columns=columns)
#
# print(df)
