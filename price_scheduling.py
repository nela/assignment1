import numpy as np
from scipy.optimize import linprog
from objects import ElAppliance
from generate_rt_prices import daily_price

def get_price_schedule_pr_appliance(appliance: ElAppliance, hourly_prices):

    # First get the prices for the subset of the operational times for
    # the appliance. If timeMin > timeMax then the appliance can be continously
    # operation over 00.00
    if appliance.timeMin > appliance.timeMax:
        double_tmp = np.append(hourly_prices, hourly_prices)
        print(double_tmp)
        hourly_prices_subset = double_tmp[appliance.timeMin:
            appliance.timeMax+len(hourly_prices)]
        hours = len(hourly_prices_subset)
        print("ssue")
        print(hourly_prices_subset)
        print(hours)
        num_possible_starting_hours = hours - appliance.duration
        print(num_possible_starting_hours)
    else:
        hourly_prices_subset = np.array(hourly_prices[appliance.timeMin:
            appliance.timeMax+1])
        hours = len(hourly_prices_subset)
        num_possible_starting_hours = hours - appliance.duration

    # Lists in which to store equality and inequality matrices for each
    # iteration. These matrices are sent to linprog in orderto determine
    # the total price for running the appliance, starting at each possible hour
    MA_ub = []
    MA_eq = []

    # These loops populate the matrices with 0 and 1 for linear optimization
    for i in range(num_possible_starting_hours + 1):
        m = np.zeros([hours, hours])
        n = np.zeros(hours)
        for j in range(appliance.duration):
            m[j+i][j+i] = 1
            n[j+i] = 1

        MA_eq.append(np.array([n]))
        MA_ub.append(np.squeeze(np.asarray(m)))

    # These are the equality and inequality results. They are the same for
    # all possible A_ub and A_eq matrices from above
    b_ub = np.full(hours,
            round(appliance.dailyUsageMax / appliance.duration, 2))
    b_eq = appliance.dailyUsageMax

    # Array that stores the total price for each hour
    prices = []

    for i in range(len(MA_eq)):
        # Extract the matrix for each hour
        A_eq = MA_eq[i]
        A_ub = MA_ub[i]

        # Send to the optimization algorithm
        res = linprog(hourly_prices_subset, A_ub, b_ub, A_eq, b_eq)

        # Calculate the product of vectors
        # The vectors are the hourly prices
        # and the kWh consumption for each hour
        prices.append(np.dot(hourly_prices_subset, res.x))

    return np.round_(prices, decimals=2)

# Generate hourly prices as in task 1
# hourly_prices = []
# for i in range(24):
#     hourly_prices.insert(i, 1) if 17 <= i <= 20 else hourly_prices.insert(i, 0.5)


# Or generate random hourly prices as per task 2
# hourly_prices = daily_price(0.2, 0.8)

# Or define them yourself so you can clearly see whats going on
# hourly_prices = [0.1, 0.1,
#         0.3, 0.2, 0.1, 0.1, 0.2, 0.1, 0.3,
#         0.3, 0.3, 0.2,0.3, 0.3, 0.3, 0.2,0.3, 0.3, 0.3, 0.2,0.3, 0.3, 0.3, 0.1]
#
# # Create an appliance object
# ev = ElAppliance("Electric Vehicle", 9.9, 9.9, 3, timeMin=21, timeMax=8)
#
# # Get the total price schedule
# price_schedule = get_price_schedule_pr_appliance(ev, hourly_prices)
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
# optimal_hour = np.argmin(price_schedule) + ev.timeMin
# print("The optimal hour with minimal price: ", optimal_hour)


dd = daily_price(0.5, 1.0)
print(dd)
