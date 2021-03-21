import numpy as np
import pandas as pd
from scipy.optimize import linprog
from classes import ElAppliance, Household, ElType


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
        b_eq.append(a.actual_consumption)

    return A_eq, b_eq


# Create vectors and matrices that define the inequality constraints
def create_ub_constraints(appliances: list, hours=24, task4=False, peak_load=None):
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

    if task4:
        if peak_load is None:
            raise ValueError("Input peak load in order to balance load")
        for h in range(hours):
            a_ub = np.zeros(hours*len(appliances))
            for i in range(0, hours*len(appliances), hours):
                a_ub[h+i] = 1

            A_ub.append(a_ub)
            b_ub.append(peak_load)

    return A_ub, b_ub


def optimization_appliance_schedule(appliances: list,
        hourly_prices: list, task4=False, peak_load=None) :
    c = []
    for i in range(len(appliances)):
        c.extend(hourly_prices)

    A_eq, b_eq = create_eq_constraints(appliances)
    A_ub, b_ub = create_ub_constraints(appliances, task4=task4, peak_load=peak_load)
    options = { 'cholesky': False, 'sym_pos': False }
    res = linprog(c, A_ub, b_ub, A_eq, b_eq, options=options)
    # res = linprog(c, A_ub, b_ub, A_eq, b_eq)
    print(res.success, '\n', res.status, '\n', res.message, '\n')
    x = np.round_(res.x, decimals=4)

    return [x[i:(i+24)] for i in range(0, len(x), 24)]
