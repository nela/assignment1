import random
from generate_rt_prices import daily_price
import numpy as np
from scipy.optimize import linprog
import enum

# creating enumerations using class
class ElType(enum.Enum):
    shiftable = 1
    shiftable_non_continious =2
    non_shiftable_non_continious = 3
    non_shiftable = 4

class ElAppliance:
    #type : 1 = shiftable, 2 = non-shiftable non-continious, 3 = non-shiftable
    def __init__(self,name,dailyUsageMin,dailyUsageMax,maxHourConsumption,duration,elType,timeMin = 0,timeMax = 23):
        self.name = name
        self.dailyUsageMin = dailyUsageMin
        self.dailyUsageMax = dailyUsageMax
        self.duration = duration
        self.timeMin = timeMin
        self.timeMax = timeMax
        self.maxHourConsumption = maxHourConsumption
        self.elType = elType

        #get a random time between min and max for dailyUsage variables.
    def randomTime(self):
            return random.randint(self.timeMin, self.timeMax)

    def randomUsage(self):
        if self.dailyUsageMin == self.dailyUsageMax:
            return self.dailyUsageMin
        return random.randint(self.dailyUsageMin, self.dailyUsageMax)

    def randomTimeDuration(self):
        if self.timeMin == self.timeMax:
            return self.timeMin
        return random.randint(self.timeMin, (self.timeMax-self.duration))


class Household:
    #constructor
    elAppliance = []
    def __init__(self, name, appliances=None):
        #inizalise
        self.name = name
        if appliances is not None:
            for a in appliances:
                self.elAppliance.append(a)


    def makeElappliances(self,number):
        elNames = ["Dishwasher","Laundry machine","Electric vehicle","Lighting","Heating", "Refrigerator-freezer","Electric stove","TV","Computer","Router","Ceiling fan", "Separate Freezer"]
        elPowerMin = [1.44,1.94,9.9,1,6.4,1.32,3.9,0.15,0.6,0.14,0.22,0.84]
        elPowerMax = [1.44,1.94,9.9,2,9.6,3.96,3.9,0.6,0.6,0.14,0.22,0.84]
        elMaxHourPower = [1.44,0.485,3.3,0.2,0.4,0.164,2,0.12,0.1,0.006,0.073,0.035]
        elDuration = [1,4,3,10,24,24,3,5,6,24,3,24]     #2.5 changed to 3
        elTimeMin = [0,0,0,9,0,0,0,0,0,0,0,0]
        elTimeMax = [24,24,24,20,24,24,24,24,24,24,24,24]
        elType = [ElType.shiftable,ElType.shiftable,ElType.shiftable,ElType.non_shiftable,ElType.non_shiftable,ElType.non_shiftable,ElType.non_shiftable_non_continious,ElType.non_shiftable_non_continious,ElType.non_shiftable_non_continious,ElType.non_shiftable,ElType.non_shiftable_non_continious,ElType.non_shiftable]
        for x in range(number):
            pick = random.randint(0, (len(elNames)-1))
            self.elAppliance.append(ElAppliance(elNames[pick],elPowerMin[pick],elPowerMax[pick],elMaxHourPower[pick],elDuration[pick],elType[pick],elTimeMin[pick],elTimeMax[pick]))


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
    #for x in hourly_prices:
        #print(">>",x)
    hourly_prices_subset = get_hourly_prices_subset(appliance, hourly_prices)
    #print(">>len(hourly_prices_subset):", len(hourly_prices_subset))
    hours = len(hourly_prices_subset)
    #print(">>hours - appliance.duration : ",hours - appliance.duration)
    num_possible_starting_hours = hours - appliance.duration

    # Lists in which to store equality and inequality matrices for each
    # iteration. These matrices are sent to linprog in orderto determine
    # the total price for running the appliance, starting at each possible hour
    MA_ub = []
    MA_eq = []

    # These loops populate the matrices with 0 and 1 for linear optimization
    #print("num_possible_starting_hours + 1 :",num_possible_starting_hours + 1)
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
    #print("len(MA_eq) : ",len(MA_eq))
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
    #print(">>> len(appliance_schedule): ",len(appliance_schedule))
    appliance_schedule_min_sorted = np.zeros(
            [len(price_hour_min_sorted),len(appliance_schedule[0])])

    # Sort and copy the appliance schedule to a new array
    # Remove the offset for the indexes to make sense
    for i in range(len(price_hour_min_sorted)):
        appliance_schedule_min_sorted[i] = appliance_schedule[
                price_hour_min_sorted[i][1]-offset]

    return price_hour_min_sorted, appliance_schedule_min_sorted


def format_24h_appliance_schedule(appliance_schedule, timeMin, timeMax):
    #print(appliance_schedule)
    l = []
    if timeMax > timeMin:
        l = [np.insert(np.append(a, np.zeros(24 - timeMax)), 0,
            np.zeros(timeMin)) for a in appliance_schedule]
    else:
        for a in appliance_schedule:
             l.append(np.concatenate((a[(24-timeMin):],
                np.zeros(timeMin-timeMax), a[:(24 - timeMin)])))
    return l


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
    # print(res)
    # print(prices)
    # print(np.sum(prices))
    return np.sum(prices), schedule


def get_sorted_price_appliance_schedule(appliance: ElAppliance, hourly_prices):
    #for x in hourly_prices:
    #    print(">",x)
    price_schedule, tmp_app_schedule = get_min_price_appliance_values(
            appliance, hourly_prices)
    #print("hei 1: ", len(tmp_app_schedule))
    price_schedule, tmp_app_schedule = min_sorted_schedule(price_schedule,
            tmp_app_schedule, appliance.timeMin)

    appliance_schedule = format_24h_appliance_schedule(tmp_app_schedule,
            appliance.timeMin, appliance.timeMax)

    return price_schedule, appliance_schedule

class Neighborhood:
    dailyPowerTimetable =[]
    houses =[]

    def updateTimetable(self,type):
        if type == "ToU":
            for x in range(24):
                if ((x >= 17) and (x <=20)):
                    self.dailyPowerTimetable.insert(x, 1)
                else:
                    self.dailyPowerTimetable.insert(x, 0.5)
        if type == "RTP":
            self.dailyPowerTimetable = daily_price(0.5,1)


    def __init__(self,name,priceScheme):
        #inizalise
        self.name = name
        #for x in range(24):
            #self.dailyPowerTimetable.append(0)
        self.updateTimetable(priceScheme)

        #methode that takes a house name and return the coresponding household object, returns None if not found
    def getHouse(self,houseName):
        for x in range(len(self.houses)):
            if self.houses[x].name is houseName:
                return self.houses[x]
        return None

    #methode that plan usage of machines for one household
    def testUseElAppliancesSolo(self,houseName):
        timeSchedule = []
        for x in range(24):
            timeSchedule.append(0)

        houseForSchedule = self.getHouse(houseName)
        priorityList = []
        for i in range(4):
            find_type_target = 4-i
            for appliance in houseForSchedule.elAppliance:
                if appliance.elType.value == find_type_target:
                    priorityList.append(appliance)

        first = True
        for temp_el in priorityList:
            print(temp_el.name," : ",temp_el.elType.value)

            #kall på optimalisering
            print("temp_el")
            print(temp_el.name)
            print(temp_el.timeMin)
            print(temp_el.timeMax)
            print("Duration")
            print(temp_el.duration)
            print("Dailypowertimetable")
            print(self.dailyPowerTimetable)
            price_schedule, appliance_schedule = get_sorted_price_appliance_schedule(temp_el,self.dailyPowerTimetable)
            #first element
            if first == True:
                for x in range(24):
                    timeSchedule[x] = appliance_schedule[0][x]
                first =False
            else:
                #find all with lowest cost
                current_lowest_value = price_schedule[0]
                same_value_number = 0
                for x in range(len(price_schedule)):
                    if current_lowest_value == price_schedule[x]:
                        same_value_number = x
                #choose best option
                current_load_on_timeslots = []
                for y in range(same_value_number):
                    find_pos =[]
                    temp_load = 0
                    for z in range(24):
                        if appliance_schedule[y][z] > 0:
                            find_pos.append(z)
                    for pos in find_pos:
                        temp_load = temp_load + timeSchedule[pos]
                    current_load_on_timeslots.append(temp_load)
                picked_opt = 0
                low = 100000000000000000000
                for tel in range(len(current_load_on_timeslots)):
                    if current_load_on_timeslots[tel] < low:
                        low = current_load_on_timeslots[tel]
                        picked_opt = tel
                for i in range(24):
                    timeSchedule[i] = timeSchedule[i] + appliance_schedule[picked_opt][i]
        return timeSchedule


    def printInfo(self,houseNumber):
        print("\nHouse Name: ", self.houses[houseNumber].name,"\n")
        for x in range(len(self.houses[houseNumber].elAppliance)):
            print(self.houses[houseNumber].elAppliance[x].name)
            print("Timeframe start:", (self.houses[houseNumber].elAppliance[x].timeMin+1))
            print("Timeframe end:", (self.houses[houseNumber].elAppliance[x].timeMax+1))
            randomTime = self.houses[houseNumber].elAppliance[x].randomTime()
            print("Actual start-time:", randomTime)
            print("Operating time in hours:", self.houses[houseNumber].elAppliance[x].duration)
            pricePerKWH = self.dailyPowerTimetable[randomTime]
            print("Total energy usage (max):", self.houses[houseNumber].elAppliance[x].dailyUsageMax)
            print("Energy price per kWh:", pricePerKWH)
            print("Energy price in total:", pricePerKWH * self.houses[houseNumber].elAppliance[x].dailyUsageMax, "\n")
