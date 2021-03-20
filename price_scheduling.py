import numpy as np
from scipy.optimize import linprog
from objects import ElAppliance


def schedule_non_continous_appliance(appliance: ElAppliance, hourly_prices):
    hours = 24
    A_ub = np.zeros([hours, hours])
    a_eq = np.zeros(hours)
    b_eq = appliance.dailyUsageMax
    b_ub = np.zeros(hours)
    if appliance.timeMax > appliance.timeMin:
        for i in range(appliance.timeMin, appliance.timeMax):
            A_ub[i][i] = 1
            a_eq[i] = 1
    else:
        for i in range(appliance.timeMin, 24):
            A_ub[i][i] = 1
            a_eq[i] = 1
        for i in range(0, appliance.timeMax):
            a_eq[i] = 1
    for i in range(len(b_ub)):
        b_ub[i] = appliance.maxHourConsumption
    A_eq = np.array([a_eq])
    res = linprog(hourly_prices, A_ub, b_ub, np.array(A_eq), b_eq)
    schedule = np.round_(res.x, decimals=2)
    prices = np.multiply(hourly_prices, schedule)
    return np.sum(prices), schedule


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

            if h > a.timeMin and h < a.timeMax:
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
    x = np.round_(res.x, decimals=2)

    return [x[i:(i+24)] for i in range(0, len(x), 24)]

def get_hourly_prices_subset(appliance: ElAppliance, hourly_prices):
    # Get the prices for the subset of the operational times for
    # the appliance. If timeMin > timeMax then the appliance can be
    # operation over 00.00

    if (appliance.timeMax > 24):
        raise ValueError("Appliance timeMax cannot be greater than 24.")
    elif(appliance.timeMax == 0):
        raise ValueError("Appliance timeMax cannot be 0. If you mean midnight \
                input 24 instead. ")

    if appliance.timeMin > appliance.timeMax:
        double_tmp = np.append(hourly_prices, hourly_prices)
        hourly_prices_subset = double_tmp[appliance.timeMin:
            appliance.timeMax+len(hourly_prices)]
    else:
        hourly_prices_subset = np.array(hourly_prices[appliance.timeMin:
            appliance.timeMax])

    print(len(hourly_prices_subset))
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


def min_sorted_schedule(price_schedule, appliance_schedule, offset):
    price_hour_tmp = []
    # The index of the minimal price is the optimal hour counting from the
    # appliances lowest operational hour, ie. appliance.timeMin.
    # Therefore if the appliance.timeMin > 0, it always the offsets the index
    # by that amount, and therefore that needs to be added in order to find the
    # hour not dependent on th appliance.timeMin
    for i in range(len(price_schedule)):
        price_hour_tmp.append((price_schedule[i], i+offset))

    price_hour_min_sorted = sorted(price_hour_tmp, key=lambda x: (x[0], x[1]))

    appliance_schedule_min_sorted = np.zeros(
            [len(price_hour_min_sorted),len(appliance_schedule[0])])

    # Sort and copy the appliance schedule to a new array
    # Remove the offset for the indexes to make sense
    for i in range(len(price_hour_min_sorted)):
        appliance_schedule_min_sorted[i] = appliance_schedule[
                price_hour_min_sorted[i][1]-offset]

    return price_hour_min_sorted, appliance_schedule_min_sorted


def format_24h_appliance_schedule(appliance_schedule, timeMin, timeMax):
    l = []
    if timeMax > timeMin:
        l = [np.insert(np.append(a, np.zeros(24 - timeMax)), 0,
            np.zeros(timeMin)) for a in appliance_schedule]
    else:
        for a in appliance_schedule:
             l.append(np.concatenate((a[(24-timeMin):],
                np.zeros(timeMin-timeMax), a[:(24 - timeMin)])))
    return l


def get_sorted_price_appliance_schedule(appliance: ElAppliance, hourly_prices):
    if (appliance.timeMax > 24):
        raise ValueError("Appliance timeMax cannot be greater than 24.")
    elif(appliance.timeMax == 0):
        raise ValueError("Appliance timeMax cannot be 0. If you mean midnight \
                input 24 instead. ")
    elif(appliance.timeMin > 23):
        raise ValueError("Appliance timeMin cannot be grater than 23. If you \
                mean midnight put 0 instead.")
    elif((appliance.timeMax - appliance.timeMin) == 1):
        raise ValueError("If you know the scheduling hour, don't use linprog")
    elif(duration  == (appliance.timeMax-appliance.timeMin)):
        raise ValueError("If you know the scheduling hour, don't use linprog")
    elif(duration > (appliance.timeMax-appliance.timeMin)):
        raise ValueError("Appliance duration cannot be larger than the operational time")

    price_schedule, tmp_app_schedule = get_min_price_appliance_values(
            appliance, hourly_prices)

    price_schedule, tmp_app_schedule = min_sorted_schedule(price_schedule,
            tmp_app_schedule, appliance.timeMin)

    appliance_schedule = format_24h_appliance_schedule(tmp_app_schedule,
            appliance.timeMin, appliance.timeMax)

    return price_schedule, appliance_schedule

<<<<<<< HEAD
# Or define them yourself so you can clearly see whats going on
hourly_prices = [0.1, 0.1,
        0.3, 0.2, 0.1, 0.1, 0.2, 0.1, 0.3,
        0.3, 0.3, 0.2,0.3, 0.3, 0.3, 0.2,0.3, 0.3, 0.3, 0.2,0.3, 0.3, 0.3, 0.1]


# Create an appliance object
ev = ElAppliance("Electric Vehicle", 9.9, 9.9, 3.3, 3, 1, timeMin=0, timeMax=23)
# prices, optimal_schedule = schedule_non_continous_appliance(ev, hourly_prices)
# print(optimal_schedule)


# Make the magic happen
price_schedule, appliance_schedule = get_sorted_price_appliance_schedule(
        ev, hourly_prices)
print(price_schedule)
print(appliance_schedule)
=======
# # Or define them yourself so you can clearly see whats going on
# hourly_prices = [0.1, 0.1,
#         0.3, 0.2, 0.1, 0.1, 0.2, 0.1, 0.3,
#         0.3, 0.3, 0.2,0.3, 0.3, 0.3, 0.2,0.3, 0.3, 0.3, 0.2,0.3, 0.3, 0.3, 0.1]
#
#
# # Create an appliance object
# ev = ElAppliance("Electric Vehicle", 9.9, 9.9, 3.3, 3, 1, timeMin=0, timeMax=23)
# # prices, optimal_schedule = schedule_non_continous_appliance(ev, hourly_prices)
# # print(optimal_schedule)
#
#
# # Make the magic happen
# price_schedule, appliance_schedule = get_sorted_price_appliance_schedule(
#         ev, hourly_prices)
# print(price_schedule)
# print(appliance_schedule)
>>>>>>> master
