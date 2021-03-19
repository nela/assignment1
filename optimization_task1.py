import numpy as np
from pandas import DataFrame
from scipy.optimize import linprog
from objects import ElAppliance, Household, ElType
import price_scheduling as ps

# Create vectors and matrices that define equality constraints
def create_eq_constraints(appliance: list, hours=24):
    A_eq, b_eq = [], []
    index = 0

    for a in appliance:
        a_eq = np.zeros(hours * len(appliance))

        for i in range(index + a.timeMin, index + a.timeMax):
            a_eq[i] = 0.7

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
                a_ub[index + h] = 0.7

            A_ub.append(a_ub)
            b_ub.append(a.maxHourConsumption)
        index += hours

    return A_ub, b_ub


def schedule_multiple_non_continuous_appliances(appliances: list,
        hourly_prices: list, bounds_strategy=None, bounds=None) :
    c = []
    for i in range(len(appliances)):
        c += hourly_prices
    power = np.full(len(c), 0.33)

    optimization_bounds = None
    if bounds_strategy is not None:
        optimization_bounds = create_optimization_bounds(bounds_strategy, bounds) * len(appliances)
    if bounds is not None:
        pass

    A_eq, b_eq = create_eq_constraints(appliances)
    A_ub, b_ub = create_ub_constraints(appliances)
    cd = np.power(c, power)
    res = linprog(cd , A_ub, b_ub, A_eq, b_eq, bounds=optimization_bounds)
    print(res)
    x = np.round_(res.x, decimals=2)

    return [x[i:(i+24)] for i in range(0, len(x), 24)]


def create_optimization_bounds(bounds_strategy, bounds=None):
    if bounds_strategy != 'static' and bounds_strategy != 'price_inverse':
        raise ValueError("Bound strategy can be either \'static\' or \'price_inverse\'.")
    elif bounds_strategy == 'static' and bounds is None:
        raise ValueError("If you wish to run with static load bounds, \
                please provide a bound threshold. {bound} variable cannot be empty.")

    optimization_bounds = []
    if bounds_strategy == 'static':
        return [(0, bounds) for i in range(24)]
    elif bounds_strategy == 'price_inverse':
        pass


def sort_appliances(appliances: list):
    shiftable_continuous = []
    shiftable_non_continuous = []
    non_shiftable = []
    for appliance in house.elAppliance:
        if appliance.elType == ElType.shiftable:
            shiftable_continuous.append(appliance)
        elif appliance.elType == ElType.shiftable_non_continious:
            shiftable_non_continuous.append(appliance)
        elif appliance.elType == ElType.non_shiftable:
            non_shiftable.append(appliance)

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


def schedule_shiftable_non_continuous(shiftable_non_continious: list, hourly_prices: list, bounds_strategy=None, bounds=None):
    schedule = schedule_multiple_non_continuous_appliances(shiftable_non_continious, hourly_prices, bounds_strategy, bounds)
    names = [a.name for a in shiftable_non_continious]

    return names, schedule


def get_house_load_schedule_depr(house: Household, hourly_prices: list):
    shiftable_continuous, shiftable_non_continuous, non_shiftable = sort_appliances(house.elAppliance)

    ns_names, ns_schedule = schedule_non_shiftable(non_shiftable)
    sc_names, sc_schedule = schedule_shiftable_continuous(shiftable_continuous, hourly_prices)
    snc_names, snc_schedule = schedule_shiftable_non_continuous(shiftable_non_continuous, hourly_prices)

    columns = ns_names + sc_names + snc_names
    schedule = ns_schedule + sc_schedule + snc_schedule

    return DataFrame([list(x) for x in zip(*schedule)], columns=columns)


def get_optimal_hours_for_continuous(appliance: ElAppliance, hourly_prices):
    cost = []
    for h in range(appliance.timeMin, appliance.timeMax):
        cost.append((sum(hourly_prices[h:(h+appliance.duration)]), h))

    sorted_cost = sorted(cost, key=lambda x: (x[0], x[1]))

    return sorted_cost[0]


def updated_hours_continuous(appliances: list, hourly_prices):
    substitutions = []
    for a in appliances:
        print(a.name)
        optimal_hour = get_optimal_hours_for_continuous(a, hourly_prices)
        print(optimal_hour)
        optimal_hour = optimal_hour[1]
        substitutions.append(ElAppliance(a.name, a.dailyUsageMin, a.dailyUsageMax,
            a.maxHourConsumption, a.duration, a.elType, optimal_hour, a.timeMax))

    return substitutions


def get_house_load_schedule(house: Household, hourly_prices: list, bounds_strategy=None, bounds=None):
    shiftable_continuous, shiftable_non_continuous, non_shiftable = sort_appliances(house.elAppliance)

    updated_continuous = updated_hours_continuous(shiftable_continuous, hourly_prices)
    optimizable = shiftable_non_continuous + updated_continuous

    ns_names, ns_schedule = schedule_non_shiftable(non_shiftable)
    snc_names, snc_schedule = schedule_shiftable_non_continuous(optimizable, hourly_prices, bounds_strategy, bounds)

    columns = ns_names + snc_names
    schedule = ns_schedule + snc_schedule

    return DataFrame([list(x) for x in zip(*schedule)], columns=columns)


def get_total_house_load(house):
    load = 0
    for a in house.elAppliance:
        load += a.dailyUsageMax

    return load

hourly_prices = [0.1, 0.1,
        0.3, 0.2, 0.1, 0.1, 0.2, 0.1, 0.3,
        0.3, 0.3, 0.2,0.3, 0.3, 0.3, 0.2,0.3, 0.3, 0.3, 0.2,0.3, 0.3, 0.3, 0.1]
lght = ElAppliance("Lighing", 1, 2, 0.2, 10, ElType.non_shiftable, timeMin=10, timeMax=20)
#
#
heat = ElAppliance("Heating", 6.4, 9.6, 0.4, 24, ElType.non_shiftable, timeMin=0, timeMax=24)
# rfrg = ElAppliance("Refrigerator", 1.32, 3.96, 0.164, 24, ElType.non_shiftable, timeMin=0, timeMax=24)
stove = ElAppliance("Stove", 3.9, 3.9, 2, 3, ElType.shiftable, timeMin=14, timeMax=22)
# tv = ElAppliance("Tv", 0.15, 0.6, 0.12, 5, ElType.non_shiftable, timeMin=17, timeMax=22)
# computer = ElAppliance("Computer", 0.6, 0.6, 0.1, 6, ElType.non_shiftable, timeMin=8, timeMax=24)
# router = ElAppliance("Router", 0.14, 0.14, 0.006, 24, ElType.non_shiftable, timeMin=0,timeMax=24)
# fan = ElAppliance("Ceiling Fan", 0.22, 0.22, 0.073, 3, ElType.shiftable_non_continious, timeMin=12, timeMax=20)
# freezer = ElAppliance("Freezer", 0.84, 0.84,  0.035, 24, ElType.non_shiftable, timeMin=0, timeMax=24)
# dw = ElAppliance("Dishwaasher", 1.44, 1.44, 1.44, 1, ElType.shiftable_non_continious, timeMin=14, timeMax=24)
# lm = ElAppliance("Laundry Machine", 1.94, 1.94, 0.485, 2, ElType.shiftable, timeMin=0, timeMax=18)
# dryer = ElAppliance("Cloth Dryer", 2.5, 2.5, 2.5, 1, ElType.shiftable, timeMin=0, timeMax=20)
ev = ElAppliance("Electric batmobile", 9.9, 9.9, 3.3, 3, ElType.shiftable, timeMin=0, timeMax=8)
ev2 = ElAppliance("Electric bitchmobile", 9.9, 9.9, 3.3, 3, ElType.shiftable_non_continious, timeMin=8, timeMax=16)
# iron = ElAppliance("Cloth Iron", 0.28, 0.28, 0.28, 1, ElType.shiftable, timeMin=10, timeMax=20)
# cellcharger = ElAppliance("Cellphone charger", 0.01, 0.01, 0.003, 1, ElType.shiftable_non_continious, timeMin=0, timeMax=12)
# mw = ElAppliance("Microwave", 0.6, 0.6, 0.6, 1, ElType.shiftable, timeMin=17, timeMax=24)
# hd = ElAppliance("Hair Dryer", 0.19, 0.19, 0.19, 1, ElType.shiftable, timeMin=19, timeMax=23)
# toaster = ElAppliance("Toaster", 0.3, 0.3, 0.3, 1, ElType.shiftable, timeMin=12, timeMax=20)


# appliances = [lght, heat, rfrg, stove, tv, computer, router, fan, freezer,
#        dw, lm, dryer, ev, iron, cellcharger, mw, hd, toaster]


appliances2 = [lght, heat, ev, stove, ev2]
house = Household("Mi Casa", appliances2)

load = get_total_house_load(house)
avg_load = get_total_house_load(house)/len(house.elAppliance)
print(avg_load)

df = get_house_load_schedule(house, hourly_prices)
print(df)

# shiftable_continuous, shiftable_non_continuous, non_shiftable = sort_appliances(house.elAppliance)
#
# res = get_optimal_hours_for_continuous(ev, hourly_prices)
# print(res)
