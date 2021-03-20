import pandas as pd
from schedule_appliances import get_house_load_schedule, get_neighbourhood_load_schedule, get_total_daily_load, get_load_schedule
from generate_rt_prices import daily_price
from classes import ElAppliance, Household, Neighbourhood, ElType


def task1():
    hourly_prices = [1 if i >= 17 and i < 20 else 0.5 for i in range(24)]

    house = []
    names = ['Electric Vehicle', 'Dishwasher', 'Laundry Machine']
    house.append(ElAppliance(names[0], 9.9, 9.9, 3.3, 3, ElType.shiftable_non_continuous, timeMin=0, timeMax=8))
    house.append(ElAppliance(names[1], 1.44, 1.44, 1.44, 1, ElType.shiftable, timeMin=14, timeMax=24))
    house.append(ElAppliance(names[2], 1.94, 1.94, 0.485, 4, ElType.shiftable, timeMin=0, timeMax=18))

    names, schedule = get_load_schedule(house, hourly_prices)
    df = pd.DataFrame([list(x) for x in zip(*schedule)], columns=names)
    print(df)


def task2():
    pass


def task3():
    pass


def task4():
    pass

task1()

