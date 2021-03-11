import numpy as np
from scipy.optimize import linprog
from objects import ElAppliance
# from generate_rt_prices import daily_price

def get_hourly_prices_subset(appliance: ElAppliance, hourly_prices):
    # Get the prices for the subset of the operational times for
    # the appliance. If timeMin > timeMax then the appliance can be
    # operation over 00.00

    if appliance.timeMin > appliance.timeMax:
        double_tmp = np.append(hourly_prices, hourly_prices)
        hourly_prices_subset = double_tmp[appliance.timeMin:
            appliance.timeMax+len(hourly_prices)]
    else:
        hourly_prices_subset = np.array(hourly_prices[appliance.timeMin:
            appliance.timeMax])

    return hourly_prices_subset


def get_min_price_appliance_values(appliance: ElAppliance, hourly_prices):
    hourly_prices_subset = get_hourly_prices_subset(appliance, hourly_prices)
    hours = len(hourly_prices_subset)
    num_possible_starting_hours = hours - appliance.duration

    # Lists in which to store equality and inequality matrices for each
    # iteration. These matrices are sent to linprog in orderto determine
    # the total price for running the appliance, starting at each possible hour
    MA_ub = []
    MA_eq = []

    # These loops populate the matrices with 0 and 1 for linear optimization
    for i in range(num_possible_starting_hours + 1):
        ub = np.zeros([hours, hours])
        eq = np.zeros(hours)
        for j in range(appliance.duration):
            ub[j+i][j+i] = 1
            eq[j+i] = 1

        MA_ub.append(np.squeeze(np.asarray(ub)))
        MA_eq.append(np.array([eq]))

    # These are the equality and inequality results. They are the same for
    # all possible A_ub and A_eq matrices from above
    b_ub = np.full(hours,
            round(appliance.dailyUsageMax / appliance.duration, 2))
    b_eq = appliance.dailyUsageMax

    # Array that stores the total price for each hour
    price_schedule = []
    appliance_schedule = []
    for i in range(len(MA_eq)):
        # Extract the matrix for each hour
        A_eq = MA_eq[i]
        A_ub = MA_ub[i]

        # Send to the optimization algorithm
        res = linprog(hourly_prices_subset, A_ub, b_ub, A_eq, b_eq)

        # Calculate the product of vectors
        # The vectors are the hourly prices
        # and the kWh consumption for each hour
        appliance_schedule.append(np.round_(res.x, decimals=2))
        price_schedule.append(np.dot(hourly_prices_subset, res.x))

    price_schedule = np.round_(price_schedule, decimals=2)

    return price_schedule, appliance_schedule


def sort_schedule(price_schedule, appliance_schedule):
    price_hour_tmp = []
    for i in range(len(price_schedule)):
        price_hour_tmp.append((price_schedule[i], i))

    price_hour_min_sorted = sorted(price_hour_tmp, key=lambda x: (x[0], x[1]))
    appliance_schedule_min_sorted = np.zeros(
            [len(price_hour_min_sorted),len(appliance_schedule[0])])

    for i in range(len(price_hour_min_sorted)):
        appliance_schedule_min_sorted[i] = appliance_schedule[price_hour_min_sorted[i][1]]

    return price_hour_min_sorted, appliance_schedule_min_sorted


def get_sorted_price_appliance_schedule(appliance: ElAppliance, hourly_prices):
    price_schedule, appliance_schedule = get_min_price_appliance_values(
            appliance, hourly_prices)

    return sort_schedule(price_schedule, appliance_schedule)


# Generate hourly prices as in task 1
# hourly_prices = []
# for i in range(24):
#     hourly_prices.insert(i, 1) if 17 <= i <= 20 else hourly_prices.insert(i, 0.5)


# Or generate random hourly prices as per task 2
# hourly_prices = daily_price(0.2, 0.8)

# Or define them yourself so you can clearly see whats going on
hourly_prices = [0.1, 0.1,
        0.3, 0.2, 0.1, 0.1, 0.2, 0.1, 0.3,
        0.3, 0.3, 0.2,0.3, 0.3, 0.3, 0.2,0.3, 0.3, 0.3, 0.2,0.3, 0.3, 0.3, 0.1]

# Create an appliance object
ev = ElAppliance("Electric Vehicle", 9.9, 9.9, 3, timeMin=1, timeMax=8)

# # Get the total price schedule
# price_schedule, appliance_schedule = get_min_price_appliance_values(ev, hourly_prices)
#
# print("Price Schedule:", price_schedule)
#
# # Find the minial price
# minimal_price = np.amin(price_schedule)
# print("Minimal total price: ", minimal_price)
#
# # The index of the minimal price is the optimal hour counting from the
# # appliances lowest operational hour, ie. appliance.timeMin.
# # Therefore if the appliance.timeMin > 0, it always the offsets the index
# # by that amount, and therefore that needs to be added in order to find the
# # hour not dependent on th appliance.timeMin
#
# optimal_index = np.argmin(price_schedule)
# optimal_hour = optimal_index + ev.timeMin
# print("The optimal hour with minimal price: ", optimal_hour)
#
# optimal_schedule = appliance_schedule[optimal_index]
# print(optimal_schedule)

price_schedule, appliance_schedule = get_sorted_price_appliance_schedule(
        ev, hourly_prices)
print(price_schedule)
print(appliance_schedule)
