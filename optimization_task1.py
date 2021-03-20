import numpy as np
from pandas import DataFrame
from scipy.optimize import linprog
from objects import ElAppliance, Household, ElType
import price_scheduling as ps
import random

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
        print("HEHEHEHEHEHEHEHEHEHEHEHEHEHEHEHE")
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
        c += hourly_prices

    A_eq, b_eq = create_eq_constraints(appliances)
    A_ub, b_ub = create_ub_constraints(appliances, task4=task4, peak_load=peak_load)
    # options = { 'cholesky': False, 'sym_pos': False }
    # res = linprog(c, A_ub, b_ub, A_eq, b_eq, options=options)
    res = linprog(c, A_ub, b_ub, A_eq, b_eq)
    # print(res)
    x = np.round_(res.x, decimals=4)

    return [x[i:(i+24)] for i in range(0, len(x), 24)]


def sort_appliances(appliances: list):
    shiftable_continuous = []
    shiftable_non_continuous = []
    non_shiftable = []
    for a in appliances:
        if a.elType == ElType.shiftable:
            shiftable_continuous.append(a)
        elif a.elType == ElType.shiftable_non_continious:
            shiftable_non_continuous.append(a)
        elif a.elType == ElType.non_shiftable:
            non_shiftable.append(a)

    return shiftable_continuous, shiftable_non_continuous, non_shiftable


def schedule_non_shiftable(non_shiftable: list, hour=24):
    schedule = []
    names = []
    for a in non_shiftable:
        s = np.zeros(hour)
        hourly_load = a.dailyUsageMax/a.duration
        for h in range(a.timeMin, a.timeMax):
            s[h] = hourly_load

        schedule.append(s)
        names.append(a.name)

    return names, schedule


def schedule_shiftable_continuous(shiftable_continuous: list, hourly_prices: list):
    schedule = []
    names = []
    for a in shiftable_continuous:
        pr_schedule, a_schedule = ps.get_sorted_price_appliance_schedule(a, hourly_prices)
        schedule.append(a_schedule[0])
        names.append(a.name)

    return names, schedule


def schedule_shiftable(shiftable_non_continious: list, hourly_prices: list, task4=False, peak_load=None):
    schedule = optimization_appliance_schedule(shiftable_non_continious, hourly_prices, task4=task4, peak_load=peak_load)
    names = [a.name for a in shiftable_non_continious]

    return names, schedule


def get_house_load_schedule_depr(house: Household, hourly_prices: list):
    shiftable_continuous, shiftable_non_continuous, non_shiftable = sort_appliances(house.elAppliance)

    ns_names, ns_schedule = schedule_non_shiftable(non_shiftable)
    sc_names, sc_schedule = schedule_shiftable_continuous(shiftable_continuous, hourly_prices)
    snc_names, snc_schedule = schedule_shiftable(shiftable_non_continuous, hourly_prices, task4=task4)

    columns = ns_names + sc_names + snc_names
    schedule = ns_schedule + sc_schedule + snc_schedule

    return DataFrame([list(x) for x in zip(*schedule)], columns=columns)


def get_optimal_hours_for_continuous(appliance: ElAppliance, hourly_prices):
    cost = []
    for h in range(appliance.timeMin, appliance.timeMax-appliance.duration):
        cost.append((sum(hourly_prices[h:(h+appliance.duration)]), h))

    sorted_cost = sorted(cost, key=lambda x: (x[0], x[1]))

    return sorted_cost[0]


def updated_hours_continuous(appliances: list, hourly_prices):
    substitutions = []
    for a in appliances:
        optimal_hour = get_optimal_hours_for_continuous(a, hourly_prices)
        optimal_hour = optimal_hour[1]
        substitutions.append(ElAppliance(a.name, a.dailyUsageMin, a.dailyUsageMax,
            a.maxHourConsumption, a.duration, a.elType, optimal_hour, optimal_hour+a.duration))

    return substitutions


def get_load_schedule(appliances: list, hourly_prices: list, task4=False, peak_load=None):
    if not task4 and peak_load is not None:
        raise ValueError("Remove the peak_load if it should not be taken into account for task4")
    elif task4 and peak_load is None:
        raise ValueError("Input peak load for task 4.")

    shiftable_continuous, shiftable_non_continuous, non_shiftable = sort_appliances(appliances)

    updated_continuous = updated_hours_continuous(shiftable_continuous, hourly_prices)
    shiftable = shiftable_non_continuous + updated_continuous

    schedule, columns = None, None

    if task4:
        columns, schedule = schedule_shiftable(non_shiftable+shiftable,
                hourly_prices, task4=task4, peak_load=peak_load)
    else:
        ns_names, ns_schedule = schedule_non_shiftable(non_shiftable)
        snc_names, snc_schedule = schedule_shiftable(shiftable, hourly_prices)

        columns = ns_names + snc_names
        schedule = ns_schedule + snc_schedule

    return DataFrame([list(x) for x in zip(*schedule)], columns=columns)



def get_neighbourhood_load_schedule(neighbourhood: list, hourly_prices):

    house_list = []
    optimizable = []
    for house in neighbourhood:
        name = house.name
        num_appliances = len(house.elAppliance)
        print(num_appliances)
        appliance_names = []
        for a in house.elAppliance:
            appliance_names.append(a.name)

        house_list.append((house.name, len(house.elAppliance), appliance_names))
        optimizable += house.elAppliance

    df = get_load_schedule(optimizable, hourly_prices, task4=None, peak_load=None)

    return df

def set_load_penalty(peak_hours: list[tuple[int, int]], penalty: float, hours=24):
    penalty_constraints = np.ones(hours)
    for peak in peak_hours:
        for h in range(peak[0], peak[1]):
            penalty_constraints[h] = penalty

    return penalty_constraints


def get_total_daily_load(house):
    total_load = 0
    for a in house.elAppliance:
        total_load += a.dailyUsageMax

    return total_load


def pick_random_appliances(appliances: list):

    num_appliances = random.randint(5, len(appliances)-1)
    used_appliances_index = []
    picked_appliances = []

    for a in range(num_appliances):
        index = random.randint(0, len(appliances)-1)
        while index in used_appliances_index:
            index = random.randint(0, len(appliances)-1)

        print(index)

        picked_appliances.append(appliances[index])
        used_appliances_index.append(index)

    return picked_appliances


def make_neighbourhood(num_houses: int, appliances: list):
    neighbourhood = []
    for h in range(num_houses):
        num_appliances = random.randint(5, len(appliances)-1)
        house = Household("House_" + str(h), random.sample(appliances, num_appliances))
        neighbourhood.append(house)
        print(house.name)
        for a in house.elAppliance:
            print(a.name)

    print(neighbourhood)
    return neighbourhood


hourly_prices = [0.1, 0.1, 0.3, 0.2, 0.1, 0.1, 0.2, 0.1, 0.3,
        0.3, 0.3, 0.2,0.3, 0.3, 0.3, 0.2,0.3, 0.3, 0.3, 0.2,0.3, 0.3, 0.3, 0.1]


lght = ElAppliance("Lighing", 1, 2, 0.2, 10, ElType.non_shiftable, timeMin=10, timeMax=20)
heat = ElAppliance("Heating", 6.4, 9.6, 0.4, 24, ElType.non_shiftable, timeMin=0, timeMax=24)
ev = ElAppliance("Electric batmobile", 9.9, 9.9, 3.3, 3, ElType.shiftable, timeMin=0, timeMax=8)
ev2 = ElAppliance("Electric bitchmobile", 9.9, 9.9, 3.3, 3, ElType.shiftable_non_continious, timeMin=8, timeMax=16)
stove = ElAppliance("Stove", 3.9, 3.9, 2, 3, ElType.shiftable, timeMin=14, timeMax=22)
rfrg = ElAppliance("Refrigerator", 1.32, 3.96, 0.164, 24, ElType.non_shiftable, timeMin=0, timeMax=24)
tv = ElAppliance("Tv", 0.15, 0.6, 0.12, 5, ElType.non_shiftable, timeMin=17, timeMax=22)
computer = ElAppliance("Computer", 0.6, 0.6, 0.1, 6, ElType.non_shiftable, timeMin=8, timeMax=24)
router = ElAppliance("Router", 0.14, 0.14, 0.006, 24, ElType.non_shiftable, timeMin=0,timeMax=24)
fan = ElAppliance("Ceiling Fan", 0.22, 0.21, 0.073, 3, ElType.shiftable_non_continious, timeMin=12, timeMax=20)
freezer = ElAppliance("Freezer", 0.84, 0.84,  0.035, 24, ElType.non_shiftable, timeMin=0, timeMax=24)
dw = ElAppliance("Dishwaasher", 1.44, 1.44, 1.44, 1, ElType.shiftable_non_continious, timeMin=14, timeMax=24)
lm = ElAppliance("Laundry Machine", 1.94, 1.94, 0.485, 4, ElType.shiftable, timeMin=0, timeMax=18)
dryer = ElAppliance("Cloth Dryer", 2.5, 2.5, 2.5, 1, ElType.shiftable, timeMin=0, timeMax=20)
iron = ElAppliance("Cloth Iron", 0.28, 0.28, 0.28, 1, ElType.shiftable, timeMin=10, timeMax=20)
cellcharger = ElAppliance("Cellphone charger", 0.01, 0.01, 0.003, 4, ElType.shiftable_non_continious, timeMin=0, timeMax=12)
mw = ElAppliance("Microwave", 0.6, 0.6, 0.6, 1, ElType.shiftable, timeMin=17, timeMax=24)
hd = ElAppliance("Hair Dryer", 0.19, 0.19, 0.19, 1, ElType.shiftable, timeMin=19, timeMax=23)
toaster = ElAppliance("Toaster", 0.3, 0.3, 0.3, 1, ElType.shiftable, timeMin=12, timeMax=20)


appliances = [lght, heat, rfrg, stove, ev, ev2, tv, computer, router, fan,
       freezer, dw, lm, dryer, iron, cellcharger, mw, hd, toaster]

appliances2 = [lght, heat, ev, stove, ev2]

house = Household("Mi Casa", appliances2)

# load = get_total_daily_load(house)
# print(load)
#
# df = get_load_schedule(house, hourly_prices)
# print(df)
#
# total_hourly_load = DataFrame(df.sum(axis=1), columns=["Load kWh"])
# print(total_hourly_load)

# Task 3
# neighbourhood = make_neighbourhood(2, appliances)
#
#
#
# df = get_neighbourhood_load_schedule(neighbourhood, hourly_prices)
# print(df)


# for h in neighbourhood:
#     print(h.name)
#     # for a in h.elAppliance:
#     #     print("\t", a.name)
#
# h0 = neighbourhood[0]
# h1 = neighbourhood[1]
#
# print("H0")
# for a in h0.elAppliance:
#     print(a.name)
#

# Task 4
df = get_load_schedule(house.elAppliance, hourly_prices)
print(df)
# df = get_load_schedule(house, hourly_prices, task4=True, peak_load=3.7)
#
# print(df)



# shiftable_continuous, shiftable_non_continuous, non_shiftable = sort_appliances(house.elAppliance)
#
# res = get_optimal_hours_for_continuous(ev, hourly_prices)
# print(res)
