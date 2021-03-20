from objects import ElAppliance, Household, Neighborhood,ElType

if __name__ == "__main__":
    #                  0 , 1 , 2 , 3 , 4 , 5 , 6 , 7 , 8 , 9 , 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23
    costPerHourToU = [0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5, 1 , 1 , 1 , 1 ,0.5,0.5,0.5]
    myNeighborhood = Neighborhood("Blindern","ToU")

    #--#Task 1#--#
    print("\n\n#-----# Task 1 #-----#\n")
    #make house for Task 1:
    task1House = Household("Oppgave1")
    task1House.elAppliance.append(ElAppliance("Dishwasher", 1.44, 1.44,1.44, 1,ElType.shiftable, 8, 17))
    task1House.elAppliance.append(ElAppliance("EV", 9.9, 9.9,3.3, 3,ElType.shiftable_non_continious, 0, 8))
    task1House.elAppliance.append(ElAppliance("WashingMachine", 1.94, 1.94,0.485, 4,ElType.shiftable, 8, 22))

    myNeighborhood.houses.append(task1House)
    #print price
    for x in range(24):
        print("Task1: Price in timeslot ",x+1," : ",myNeighborhood.dailyPowerTimetable[x])
    print("\n")
    #run scheduling methode for Task 1 house
    test_list = myNeighborhood.testUseElAppliancesSolo("Oppgave1")
    for x in range(len(test_list)):
        print("Task1: Powerload hour ",x+1," : ",test_list[x])

    #--#Task 2#--#
    print("\n\n#-----# Task 2 #-----#\n")
    #change price scheme to Real Time Pricing
    myNeighborhood.updateTimetable("RTP")
    #print price
    for x in range(24):
        print("Task2: Price in timeslot ",x+1," : ",myNeighborhood.dailyPowerTimetable[x])
    print("\n")
    #make blueprint for house for Task 2,Task 3 and Task 4
    blueprintHouse =Household("Blueprint")
    blueprintHouse.elAppliance.append(ElAppliance("Dishwasher", 1.44, 1.44,1.44, 1,ElType.shiftable, 8, 17))
    blueprintHouse.elAppliance.append(ElAppliance("WashingMachine", 1.94, 1.94,0.485, 4,ElType.shiftable, 8, 22))
    blueprintHouse.elAppliance.append(ElAppliance("Cloth dryer",2.5,2.5,2.5,1,ElType.shiftable,18,22))
    blueprintHouse.elAppliance.append(ElAppliance("Lighting",1,2,0.2,10,ElType.non_shiftable,9,20))
    blueprintHouse.elAppliance.append(ElAppliance("Heating",6.4,9.6,0.4,24,ElType.non_shiftable,0,24))
    blueprintHouse.elAppliance.append(ElAppliance("Refrigerator-freezer",1.32,3.96,0.164,24,ElType.non_shiftable,0,24))
    blueprintHouse.elAppliance.append(ElAppliance("Electric stove",3.9,3.9,2,3,ElType.non_shiftable_non_continious,15,20))
    blueprintHouse.elAppliance.append(ElAppliance("TV",0.15,0.6,0.2,5,ElType.non_shiftable_non_continious,12,24))
    blueprintHouse.elAppliance.append(ElAppliance("Computer",0.6,0.6,0.1,6,ElType.non_shiftable_non_continious,8,24))

    #make house for Task 2
    task2House = blueprintHouse
    task2House.name = "Oppgave2"
    task2House.elAppliance.append(ElAppliance("EV", 9.9, 9.9,3.3, 3,ElType.shiftable_non_continious, 0, 8))
    task2House.makeElappliancesAux(5) #gives 5 random ElAppliances for the house
    myNeighborhood.houses.append(task2House)
    for x in range(len(task2House.elAppliance)):
        print(">name : ", task2House.elAppliance[x].name," ElType : ",task2House.elAppliance[x].elType.value)
    print("\n")

    #run scheduling for task2House
    test_list = myNeighborhood.testUseElAppliancesSolo("Oppgave2")
    for x in range(len(test_list)):
        print("Task2: Powerload hour ",x+1," : ",test_list[x])
    test_list2 = myNeighborhood.testUseElAppliancesSolo2("Oppgave2")
    for x in range(len(test_list2)):
        print("Task2: Powerload hour ",x+1," : ",test_list2[x])

    #--#Task 3#--#
    print("\n\n#-----# Task 3 #-----#\n")
    #make neigbourhood for task 3
    task3Neighborhood = Neighborhood("Majorstua","RTP")

    #for test
    #hourly_prices = [0.1, 0.1, 0.3, 0.2, 0.1, 0.1, 0.2, 0.1, 0.3,   0.3, 0.3, 0.2,0.3, 0.3, 0.3, 0.2,0.3, 0.3, 0.3, 0.2,0.3, 0.3, 0.3, 0.1]
    #task3Neighborhood.dailyPowerTimetable = hourly_prices
    #print price
    for x in range(24):
        print("Task3: Price in timeslot ",x+1," : ",task3Neighborhood.dailyPowerTimetable[x])
    print("\n")
    #fill Neighborhood with 30 houses
    for x in range(3):
        task3House = blueprintHouse
        task3House.name = str(x)
        if ((x % 4) == 0): #give some houses Electronic Vehicle
            task3House.elAppliance.append(ElAppliance("EV", 9.9, 9.9,3.3, 3,ElType.shiftable_non_continious, 0, 8))
        #task3House.makeElappliancesAux(5)
        task3Neighborhood.houses.append(task3House)


    #run scheduling methode for Neighborhood
    test_list = task3Neighborhood.testUseElAppliancesMulti()
    for x in range(len(test_list)):
        print("Task3: Powerload hour ",x+1," : ",test_list[x])
