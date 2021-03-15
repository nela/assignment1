import random
from generate_rt_prices import daily_price
from price_scheduling import get_price_schedule_pr_appliance
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
    elAppliance = []

    #constructor
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
        elTimeMax = [23,23,23,19,23,23,23,23,23,23,23,23]
        elType = [ElType.shiftable,ElType.shiftable,ElType.shiftable,ElType.non_shiftable,ElType.non_shiftable,ElType.non_shiftable,ElType.non_shiftable_non_continious,ElType.non_shiftable_non_continious,ElType.non_shiftable_non_continious,ElType.non_shiftable,ElType.non_shiftable_non_continious,ElType.non_shiftable]
        for x in range(number):
            pick = random.randint(0, (len(elNames)-1))
            self.elAppliance.append(ElAppliance(elNames[pick],elPowerMin[pick],elPowerMax[pick],elMaxHourPower[pick],elDuration[pick],elType[pick],elTimeMin[pick],elTimeMax[pick]))


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
        for x in range(24):
            self.dailyPowerTimetable.append(0)
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
            price_schedule, appliance_schedule = get_price_schedule_pr_appliance(temp_el,dailyPowerTimetable)
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
