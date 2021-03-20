import copy
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
            return random.randint(self.timeMin, self.timeMax-1)

    def randomUsage(self):
        if self.dailyUsageMin == self.dailyUsageMax:
            return self.dailyUsageMin
        return random.randint(self.dailyUsageMin, self.dailyUsageMax)

    def randomTimeDuration(self):
        if self.timeMin == self.timeMax:
            return self.timeMin
        return random.randint(self.timeMin, (self.timeMax-1-self.duration))


class Household:
    #constructor
    def __init__(self, name, appliances=None):
        #inizalise
        if appliances is not None:
            self.elAppliance = copy.deepcopy(appliances)
        else:
            self.elAppliance = []

        self.name = name

        # if appliances is not None:
        #     for a in appliances:
        #         self.elAppliance.append(a)


    #improved methode of makeElappliances for task 2,3 and 4 house
    def makeElappliancesAux(self,number):
        elNames = ["Electric vehicle","TV","Computer","Router","Ceiling fan", "Separate Freezer","Hair dryer","Toaster","Microwave","Cellphone charger","Cloth iron"]
        elPowerMin = [9.9,0.15,0.6,0.14,0.22,0.84,0.19,0.30,0.6,0.01,0.28]
        elPowerMax = [9.9,0.6,0.6,0.14,0.22,0.84,0.19,0.30,0.6,0.01,0.28]
        elMaxHourPower = [3.3,0.2,0.1,0.006,0.073,0.035,0.19,0.30,0.6,0.003,0.28]
        elDuration = [3,5,6,24,3,24,1,1,1,3,1]
        elTimeMin = [0,12,8,0,11,0,8,8,16,0,19]
        elTimeMax = [8,24,24,24,18,24,21,12,19,8,21]
        elType = [ElType.shiftable_non_continious,ElType.non_shiftable_non_continious,ElType.non_shiftable_non_continious,ElType.non_shiftable,ElType.non_shiftable_non_continious,ElType.non_shiftable,ElType.shiftable,ElType.shiftable,ElType.shiftable,ElType.shiftable_non_continious,ElType.shiftable]
        for x in range(number):
            pick = random.randint(0, (len(elNames)-1))
            self.elAppliance.append(ElAppliance(elNames[pick],elPowerMin[pick],elPowerMax[pick],elMaxHourPower[pick],elDuration[pick],elType[pick],elTimeMin[pick],elTimeMax[pick]))


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

            if h >= a.timeMin and h < a.timeMax:
                a_ub[index + h] = 1

            A_ub.append(a_ub)
            b_ub.append(a.maxHourConsumption)
        index += hours

    return A_ub, b_ub


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

    optimization_bounds = None
    if bounds_strategy is not None:
        optimization_bounds = create_optimization_bounds(bounds_strategy, bounds) * len(appliances)
    if bounds is not None:
        pass

    A_eq, b_eq = create_eq_constraints(appliances)
    A_ub, b_ub = create_ub_constraints(appliances)
    res = linprog(c, A_ub, b_ub, A_eq, b_eq, bounds=optimization_bounds)
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
    elif(appliance.timeMin > 23):
        raise ValueError("Appliance timeMin cannot be grater than 23. If you \
                mean midnight put 0 instead.")

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
    price_schedule, tmp_app_schedule = get_min_price_appliance_values(
            appliance, hourly_prices)

    price_schedule, tmp_app_schedule = min_sorted_schedule(price_schedule,
            tmp_app_schedule, appliance.timeMin)

    appliance_schedule = format_24h_appliance_schedule(tmp_app_schedule,
            appliance.timeMin, appliance.timeMax)

    return price_schedule, appliance_schedule

class Neighborhood:


    def updateTimetable(self,el_type):
        if el_type == "ToU":
            for x in range(24):
                if ((x >= 17) and (x <=20)):
                    self.dailyPowerTimetable.insert(x, 1)
                else:
                    self.dailyPowerTimetable.insert(x, 0.5)
        if el_type == "RTP":
            self.dailyPowerTimetable = daily_price(0.5,1)


    def __init__(self,name,priceScheme):
        #inizalise
        self.name = name
        self.dailyPowerTimetable =[]
        self.houses =[]
        #for x in range(24):
            #self.dailyPowerTimetable.append(0)
        self.updateTimetable(priceScheme)

        #methode that takes a house name and return the coresponding household object, returns None if not found
    def getHouse(self,houseName):
        for x in range(len(self.houses)):
            if self.houses[x].name is houseName:
                return self.houses[x]
        return None

    #help methode for testUseElAppliancesSoloNon and testUseElAppliancesMultiNon
    #it does all the handeling for appilances of ElType 2 and 3
    def do_Non_Continious(self,timeSchedule, priorityListNonCont):
        temp_schedule = timeSchedule
        non_appliance_schedule = schedule_multiple_non_continuous_appliances(priorityListNonCont,self.dailyPowerTimetable)
        for y in range(len(non_appliance_schedule)):
            #print("non_appliance_schedule",y," : ",non_appliance_schedule[y])
            for x in range(24):
                temp_schedule[x] = temp_schedule[x] + non_appliance_schedule[y][x]
        return temp_schedule

    #help methode for testUseElAppliancesSoloNon and testUseElAppliancesMultiNon
    #it does all the handeling for appilances of ElType 1 and 4
    def do_Continious(self,timeSchedule,elAppliance):
        temp_schedule = timeSchedule

        #kall på optimalisering
        price_schedule, appliance_schedule = get_sorted_price_appliance_schedule(elAppliance,self.dailyPowerTimetable)
        #find all with lowest cost
        current_lowest_value = price_schedule[0][0]
        same_value_number = 0
        for x in range(len(price_schedule)):
            if current_lowest_value == price_schedule[x][0]:
                same_value_number = x+1
        #choose best option
        current_load_on_timeslots = []
        for y in range(same_value_number):
            find_pos =[]
            temp_load = 0
            for z in range(24):
                if appliance_schedule[y][z] > 0:
                    find_pos.append(z)
            for pos in find_pos:
                temp_load = temp_load + temp_schedule[pos]
            current_load_on_timeslots.append(temp_load)
        picked_opt = 0
        low = 100000000000000000000
        for tel in range(len(current_load_on_timeslots)):
            if current_load_on_timeslots[tel] < low:
                low = current_load_on_timeslots[tel]
                picked_opt = tel
        for i in range(24):
            temp_schedule[i] = temp_schedule[i] + appliance_schedule[picked_opt][i]
        return temp_schedule

    #uten priority
    def testUseElAppliancesSolo2(self,houseName):
        timeSchedule = []
        for x in range(24):
            timeSchedule.append(0)

        houseForSchedule = self.getHouse(houseName)
        if houseForSchedule is None:
            print("No house with that Name : ",houseName)
            return None

        priorityListNonCont = []

        #for loop to sort so ElType with a higher value gets placed first in timeSchedule
        for appliance in houseForSchedule.elAppliance:
            if appliance.elType.value == 2 or appliance.elType.value == 3:
                priorityListNonCont.append(appliance)

        #for loop through all elAppliances sorted in previous for loop with call on relevant optimization methode
        ones = True
        for teller in range(len(houseForSchedule.elAppliance)):
            if (houseForSchedule.elAppliance[teller].elType.value == 4) or (houseForSchedule.elAppliance[teller].elType.value == 1):
                temp_schedule = self.do_Continious(timeSchedule,houseForSchedule.elAppliance[teller])
                for x in range(24):
                    timeSchedule[x] = temp_schedule[x]
            elif(((houseForSchedule.elAppliance[teller].elType.value == 3) or (houseForSchedule.elAppliance[teller].elType.value == 2))and ones is True):
                temp_schedule = self.do_Non_Continious(timeSchedule,priorityListNonCont)
                for x in range(24):
                    timeSchedule[x] = temp_schedule[x]
                ones = False

        return timeSchedule

    #methode that plan usage of machines for one household
    def testUseElAppliancesSolo(self,houseName):
        timeSchedule = []
        for x in range(24):
            timeSchedule.append(0)

        houseForSchedule = self.getHouse(houseName)
        if houseForSchedule is None:
            print("No house with that Name : ",houseName)
            return None

        priorityListCont = []
        priorityListNonCont = []

        #for loop to sort so ElType with a higher value gets placed first in timeSchedule
        first = True
        for i in range(4):
            find_type_target = 4-i
            for appliance in houseForSchedule.elAppliance:
                if appliance.elType.value == find_type_target:
                    if appliance.elType.value == 2 or appliance.elType.value == 3:
                        if first is True:
                            priorityListCont.append(appliance)
                            first = False
                        priorityListNonCont.append(appliance)
                    else:
                        priorityListCont.append(appliance)

        #for loop through all elAppliances sorted in previous for loop with call on relevant optimization methode
        for teller in range(len(priorityListCont)):
            if (priorityListCont[teller].elType.value == 4) or (priorityListCont[teller].elType.value == 1):
                temp_schedule = self.do_Continious(timeSchedule,priorityListCont[teller])
                for x in range(24):
                    timeSchedule[x] = temp_schedule[x]
            elif(priorityListCont[teller].elType.value == 3) or (priorityListCont[teller].elType.value == 2):
                temp_schedule = self.do_Non_Continious(timeSchedule,priorityListNonCont)
                for x in range(24):
                    timeSchedule[x] = temp_schedule[x]

        return timeSchedule

    #methode that plan usage of machines for one household
    def testUseElAppliancesMulti(self):
        timeSchedule = []
        for x in range(24):
            timeSchedule.append(0)

        priorityListCont = []
        priorityListNonCont =[]
        first = True

        for i in range(4):
            find_type_target = 4-i
            for temp_house in self.houses:
                for appliance in temp_house.elAppliance:
                    if appliance.elType.value == find_type_target:
                        if appliance.elType.value == 2 or appliance.elType.value == 3:
                            if first is True:
                                priorityListCont.append(appliance)
                                first = False
                            priorityListNonCont.append(appliance)
                        else:
                            priorityListCont.append(appliance)

        for teller in range(len(priorityListCont)):
            if (priorityListCont[teller].elType.value == 4) or (priorityListCont[teller].elType.value == 1):
                temp_schedule = self.do_Continious(timeSchedule,priorityListCont[teller])
                for x in range(24):
                    timeSchedule[x] = temp_schedule[x]
            elif(priorityListCont[teller].elType.value == 3) or (priorityListCont[teller].elType.value == 2):
                temp_schedule = self.do_Non_Continious(timeSchedule,priorityListNonCont)
                for x in range(24):
                    timeSchedule[x] = temp_schedule[x]

        return timeSchedule


    def printInfo(self,houseName):
        printHouse = self.getHouse(houseName)
        if printHouse is None:
            print("No house with that Name : ",houseName)
            return None

        print("\nHouse Name: ", printHouse.name,"\n")
        print("ElAppliance list:")
        for x in range(len(printHouse.elAppliance)):
            print(printHouse.elAppliance[x].name)
            print("Timeframe start:", (printHouse.elAppliance[x].timeMin+1))
            print("Timeframe end:", (printHouse.elAppliance[x].timeMax))
            print("Max Hourly Consumption: ", print.elAppliance[x].maxHourConsumption)
            print("Operating time in hours:", printHouse.elAppliance[x].duration)
