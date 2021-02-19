import random


class ElApplience:
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

    def randomUsageDuration(self):
        if self.dailyUsageMin == self.dailyUsageMax:
            return self.dailyUsageMin
        return random.randint(self.dailyUsageMin, (self.dailyUsageMax-self.duration))

class Household:
    elAppliences = []

    def __init__(self,name):
        #inizalise
        self.name = name

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
        for x in range(len(self.houses[houseNumber].elAppliences)):
            print(self.houses[houseNumber].elAppliences[x].name)
            print("Timeframe start:", (self.houses[houseNumber].elAppliences[x].timeMin+1))
            print("Timeframe end:", (self.houses[houseNumber].elAppliences[x].timeMax+1))
            randomTime = self.houses[houseNumber].elAppliences[x].randomTime()
            print("Actual start-time:", randomTime)
            print("Operating time in hours:", self.houses[houseNumber].elAppliences[x].duration)
            pricePerKWH = self.dailyPowerTimetable[randomTime]
            print("Total energy usage (max):", self.houses[houseNumber].elAppliences[x].dailyUsageMax)
            print("Energy price per kWh:", pricePerKWH)
            print("Energy price in total:", pricePerKWH * self.houses[houseNumber].elAppliences[x].dailyUsageMax, "\n")


if __name__ == "__main__":
    #                  0 , 1 , 2 , 3 , 4 , 5 , 6 , 7 , 8 , 9 , 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23
    costPerHourToU = [0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5, 1 , 1 , 1 , 1 ,0.5,0.5,0.5]
    myNeighborhood = Neighborhood("Blindern","ToU")

    myHouse = Household("test")
    myHouse.elAppliences.append(ElApplience("Dishwasher", 1.44, 1.44, 1, 0, 23))
    myHouse.elAppliences.append(ElApplience("EV", 9.9, 9.9, 3, 0, 23))
    myHouse.elAppliences.append(ElApplience("WashingMachine", 1.94, 1.94, 1, 0, 23))

    myNeighborhood.houses.append(myHouse)

    for x in range(len(myNeighborhood.houses)):
        myNeighborhood.printInfo(x)
    
