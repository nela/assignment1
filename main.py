from objects import ElAppliance, Household, Neighborhood,ElType

if __name__ == "__main__":
    #                  0 , 1 , 2 , 3 , 4 , 5 , 6 , 7 , 8 , 9 , 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23
    costPerHourToU = [0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5, 1 , 1 , 1 , 1 ,0.5,0.5,0.5]
    myNeighborhood = Neighborhood("Blindern","ToU")

    #--#Task 1#--#
    print("\n\n#-----# Task 1 #-----#\n")
    #make house for Task 1:
    myHouse = Household("Oppgave1")
    myHouse.elAppliance.append(ElAppliance("Dishwasher", 1.44, 1.44,1.44, 1,ElType.shiftable, 8, 17))
    myHouse.elAppliance.append(ElAppliance("EV", 9.9, 9.9,3.3, 3,ElType.shiftable_non_continious, 0, 8))
    myHouse.elAppliance.append(ElAppliance("WashingMachine", 1.94, 1.94,0.485, 4,ElType.shiftable, 8, 22))

    myNeighborhood.houses.append(myHouse)

    test_list = myNeighborhood.testUseElAppliancesSolo("Oppgave1")
    for x in range(len(test_list)):
        print("powerload hour ",x+1," : ",test_list[x])

    #--#Task 2#--#
    print("\n\n#-----# Task 2 #-----#\n")
    #change price scheme to Real Time Pricing
    myNeighborhood.updateTimetable("RTP")
    #make blueprint for house for Task 2,Task 3 and Task 4
    blueprintHouse =Household("Blueprint")
    blueprintHouse.elAppliance.append(ElAppliance("Dishwasher", 1.44, 1.44,1.44, 1,ElType.shiftable, 8, 17))
    #blueprintHouse.elAppliance.append(ElAppliance("EV", 9.9, 9.9,3.3, 3,ElType.shiftable_non_continious, 0, 8))
    blueprintHouse.elAppliance.append(ElAppliance("WashingMachine", 1.94, 1.94,0.485, 4,ElType.shiftable, 8, 22))
    blueprintHouse.elAppliance.append(ElAppliance("Cloth dryer",2.5,2.5,2.5,1,ElType.shiftable,18,22))
    blueprintHouse.elAppliance.append(ElAppliance("Lighting",1,2,0.2,10,ElType.non_shiftable,9,20))
    blueprintHouse.elAppliance.append(ElAppliance("Heating",6.4,9.6,0.4,24,ElType.non_shiftable,0,24))
    blueprintHouse.elAppliance.append(ElAppliance("Refrigerator-freezer",1.32,3.96,0.164,24,ElType.non_shiftable,0,24))
    blueprintHouse.elAppliance.append(ElAppliance("Electric stove",3.9,3.9,2,3,ElType.non_shiftable_non_continious,15,20))
    blueprintHouse.elAppliance.append(ElAppliance("TV",0.15,0.6,0.12,5,ElType.non_shiftable_non_continious,12,24))
    blueprintHouse.elAppliance.append(ElAppliance("Computer",0.6,0.6,0.1,6,ElType.non_shiftable_non_continious,8,24))

    task2House = blueprintHouse
    task2House.name = "Oppgave2"
    task2House.elAppliance.append(ElAppliance("EV", 9.9, 9.9,3.3, 3,ElType.shiftable_non_continious, 0, 8))
    task2House.makeElappliancesAux(5)

    myNeighborhood.houses.append(task2House)
    test_list = myNeighborhood.testUseElAppliancesSolo("Oppgave2")
    for x in range(len(test_list)):
        print("powerload hour ",x+1," : ",test_list[x])

    #for x in range(len(myNeighborhood.dailyPowerTimetable)):
    #    print("daily price hour ",x+1," : ",myNeighborhood.dailyPowerTimetable[x])

    #for x in range(len(myNeighborhood.houses)):
    #    myNeighborhood.printInfo(x)
    #for x in myNeighborhood.dailyPowerTimetable:
        #print(x)

    #test_list = myNeighborhood.testUseElAppliancesSoloNon("Oppgave1")
    #for x in range(len(test_list)):
    #    print("powerload hour ",x+1," : ",test_list[x])

    #test_list = myNeighborhood.testUseElAppliancesMulti()
    #for x in range(len(test_list)):
    #    print("powerload hour ",x+1," : ",test_list[x])
    #myNeighborhood.testUseElAppliancesSolo("test")
    #print(myNeighborhood.getHouse("test").name)
    #print(myNeighborhood.getHouse("testt") is None)
