import sys
import pandas as pd
from schedule_appliances import get_house_load_schedule, \
        get_neighbourhood_load_schedule, get_total_daily_load, \
        get_load_schedule, get_hourly_load, get_total_daily_load_neigbourhood
from generate_rt_prices import daily_price
from classes import ElAppliance, Household, Neighbourhood, ElType


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

# Hourly prices generated from daily_prices, min=0.2, max=0.99
hourly_prices = [0.2232432246591243,
        0.21439749417395604,
        0.22646127290367132,
        0.2019058902183628,
        0.2084472736282907,
        0.217188222977618,
        0.4834991686820009,
        0.6614948649077409,
        0.7969147784703379,
        0.7889633962332405,
        0.7784351162092065,
        0.6715152581213365,
        0.6598643685558833,
        0.5418542497470702,
        0.2330862791045794,
        0.21737128775227166,
        0.27858552538272263,
        0.31757909999476114,
        0.7331633241955074,
        0.6566771124454189,
        0.6342015945540525,
        0.5269793292089976,
        0.4775919568309417,
        0.44726107193671527]


def task1():
    task1_prices = [1 if i >= 17 and i < 20 else 0.5 for i in range(24)]

    house = []
    names = ['Electric Vehicle', 'Dishwasher', 'Laundry Machine']
    house.append(ElAppliance(names[0], 9.9, 9.9, 3.3, 3, ElType.shiftable_non_continuous, timeMin=0, timeMax=8))
    house.append(ElAppliance(names[1], 1.44, 1.44, 1.44, 1, ElType.shiftable, timeMin=8, timeMax=17))
    house.append(ElAppliance(names[2], 1.94, 1.94, 0.485, 4, ElType.shiftable, timeMin=8, timeMax=22))

    names, schedule = get_load_schedule(house, task1_prices)
    df = pd.DataFrame([list(x) for x in zip(*schedule)], columns=names)
    print_prices(task1_prices)
    print(df)


def task2(single=False):
    house = Household("My House", single=single)

    schedule = get_house_load_schedule(house, hourly_prices)
    total_daily_load = get_total_daily_load(house)
    total_hourly_load = get_hourly_load(schedule)

    print_prices(hourly_prices)
    print(f'Total Daily Load for {house.name}:\t{total_daily_load} kWh.')
    print(schedule)
    print(total_hourly_load)


def task3(num_houses):
    neighbourhood = Neighbourhood("Blindern", num_houses)
    schedule = get_neighbourhood_load_schedule(neighbourhood, hourly_prices)
    total_daily_load = get_total_daily_load_neigbourhood(neighbourhood)
    total_hourly_load = get_hourly_load(schedule)

    print_prices(hourly_prices)
    print(f'Total Daily Load for {neighbourhood.name}:\t{total_daily_load} kWh.')
    print(schedule)
    print(total_hourly_load)


def task4(peak_load, single=False):
    house = Household("My House", single=single)
    schedule = get_house_load_schedule(house, hourly_prices, task4=True,
            peak_load=peak_load)
    total_daily_load = get_total_daily_load(house)
    total_hourly_load = get_hourly_load(schedule)

    print_prices(hourly_prices)
    print(f'Total Daily Load for {house.name}:\t{total_daily_load} kWh.')
    print(schedule)
    print(total_hourly_load)


def print_prices(prices):
    df = pd.DataFrame(prices, columns=["Hourly Prices"])
    print(df)


if len(sys.argv) < 2:
    print('Run the script with \'python solution.py --task1 || --task2 || \
            --task3 || --task4 <peak_load: float>\' ')
elif sys.argv[1] == '--task1':
    task1()
elif sys.argv[1] == '--task2':
    if len(sys.argv) < 3:
        task2(False)
    elif sys.argv[2] == 'single':
        task2(True)
elif sys.argv[1] == '--task3':
    if len(sys.argv) != 3:
        raise ValueError('Invalid number of houses. Enter a number')
    print(f'Number of houses: {sys.argv[2]}')
    task3(int(sys.argv[2]))
elif sys.argv[1] == '--task4':
    if len(sys.argv) < 3:
        raise ValueError('Invalid peak_load. Enter a number')
    print(f'Peak Load:\t{sys.argv[2]}')
    if len(sys.argv) != 4:
        task4(sys.argv[2], False)
    elif sys.argv[3] == 'single':
        task4(sys.argv[2], True)
