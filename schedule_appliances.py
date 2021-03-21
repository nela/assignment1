import numpy as np
import pandas as pd
from format_appliance_lists import get_optimal_hours_for_continuous, sort_appliances, updated_hours_continuous
from optimization import optimization_appliance_schedule


def get_total_daily_load(house):
    total_load = 0
    for a in house.elAppliance:
        total_load += a.dailyUsageMax

    return total_load


def get_total_daily_load_neigbourhood(neighbourhood):
    total_load = 0
    for house in neighbourhood.houses:
        total_load += get_total_daily_load(house)

    return total_load

def get_neighbourhood_load_schedule(neighbourhood, hourly_prices):
    house_list = []
    optimizable = []
    for house in neighbourhood.houses:
        for a in house.elAppliance:
            a.name = (house.name, a.name)

        shiftable_continuous, shiftable_non_continuous, non_shiftable = sort_appliances(house.elAppliance)

        updated_continuous = updated_hours_continuous(shiftable_continuous, hourly_prices)
        shiftable = shiftable_non_continuous + updated_continuous

        optimizable.extend(non_shiftable + shiftable)

    names, schedule = schedule_shiftable(optimizable, hourly_prices, task4=False,
            peak_load=None)

    columns = pd.MultiIndex.from_tuples(names)

    return pd.DataFrame([list(x) for x in zip(*schedule)],
            columns=columns)


def get_load_schedule(appliances: list, hourly_prices: list, task4=False, peak_load=None):
    if not task4 and peak_load is not None:
        raise ValueError("Remove the peak_load if it should not be taken into account for task4")
    elif task4 and peak_load is None:
        raise ValueError("Input peak load for task 4.")

    shiftable_continuous, shiftable_non_continuous, non_shiftable = sort_appliances(appliances)

    updated_continuous = updated_hours_continuous(shiftable_continuous, hourly_prices)
    shiftable = shiftable_non_continuous + updated_continuous

    names, schedule = None, None

    if task4:
        names, schedule = schedule_shiftable(non_shiftable+shiftable,
                hourly_prices, task4=task4, peak_load=peak_load)
    else:
        ns_names, ns_schedule = schedule_non_shiftable(non_shiftable)
        snc_names, snc_schedule = schedule_shiftable(shiftable, hourly_prices)

        names = ns_names + snc_names
        schedule = ns_schedule + snc_schedule

    return names, schedule


def get_house_load_schedule(house, hourly_prices, task4=False, peak_load=None):
    names, schedule = get_load_schedule(house.elAppliance, hourly_prices,
            task4=task4, peak_load=peak_load)

    return pd.DataFrame([list(x) for x in zip(*schedule)], columns=names)



def schedule_shiftable(shiftable_non_continious: list, hourly_prices: list, task4=False, peak_load=None):
    schedule = optimization_appliance_schedule(shiftable_non_continious, hourly_prices, task4=task4, peak_load=peak_load)
    names = [a.name for a in shiftable_non_continious]

    return names, schedule


def schedule_non_shiftable(non_shiftable: list, hour=24):
    schedule = []
    names = []
    for a in non_shiftable:
        s = np.zeros(hour)
        hourly_load = a.actual_consumption/a.duration
        for h in range(a.timeMin, a.timeMax):
            s[h] = hourly_load

        schedule.append(s)
        names.append(a.name)

    return names, schedule


def get_hourly_load(house: pd.DataFrame):
    return pd.DataFrame(house.sum(axis=1), columns=['Hourly Load kWh'])
