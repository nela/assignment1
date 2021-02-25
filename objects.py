import random


class ElAppliance:
    def __init__(self,name,dailyUsageMin,dailyUsageMax,duration,timeMin = 0,timeMax = 23):
        self.name = name
        self.dailyUsageMin = dailyUsageMin
        self.dailyUsageMax = dailyUsageMax
        self.duration = duration
        self.timeMin = timeMin
        self.timeMax = timeMax

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

    #methode that plan usage of machine
    def testUseElAppliances(self):
        timeScedule = []
        for x in range(24):
            self.timeScedule.append(0)
            # smart way, find hardest to place first, dumb way ,just put them in
            # hard to place hirarcy:
            # 1:strict timeslot(timeMin == timeMax or timeMin == timeMax-duration)
            # 2:long duration with timerestriction
            # 3:
        for x in elAppliance:
            pass


    def makeElappliances(self,number):
        elNames = ["Dishwasher","Laundry machine","Electric vehicle","Lighting","Heating", "Refrigerator-freezer","Electric stove","TV","Computer","Router","Ceiling fan", "Separate Freezer"]
        elPowerMin = [1.44,1.94,9.9,1,6.4,1.32,3.9,0.15,0.6,0.14,0.22,0.84]
        elPowerMax = [1.44,1.94,9.9,2,9.6,3.96,3.9,0.6,0.6,0.14,0.22,0.84]
        elDuration = [1,4,3,10,24,24,3,5,6,24,3,24]     #2.5 changed to 3
        elTimeMin = [0,0,0,9,0,0,0,0,0,0,0,0]
        elTimeMax = [23,23,23,19,23,23,23,23,23,23,23,23]
        for x in range(number):
            pick = random.randint(0, (len(elNames)-1))
            self.elAppliance.append(ElAppliance(elNames[pick],elPowerMin[pick],elPowerMax[pick],elDuration[pick],elTimeMin[pick],elTimeMax[pick]))


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

    def __init__(self,name,priceScheme):
        #inizalise
        self.name = name
        for x in range(24):
            self.dailyPowerTimetable.append(0)
        self.updateTimetable(priceScheme)

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
