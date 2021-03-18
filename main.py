from objects import ElAppliance, Household, Neighborhood,ElType

if __name__ == "__main__":
    #                  0 , 1 , 2 , 3 , 4 , 5 , 6 , 7 , 8 , 9 , 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23
    costPerHourToU = [0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5, 1 , 1 , 1 , 1 ,0.5,0.5,0.5]
    myNeighborhood = Neighborhood("Blindern","ToU")

    #make house for Task 1:
    myHouse = Household("Oppgave1")
    myHouse.elAppliance.append(ElAppliance("Dishwasher", 1.44, 1.44,1.44, 1,ElType.shiftable, 8, 17))
    myHouse.elAppliance.append(ElAppliance("EV", 9.9, 9.9,3.3, 3,ElType.shiftable_non_continious, 0, 8))
    myHouse.elAppliance.append(ElAppliance("WashingMachine", 1.94, 1.94,0.485, 4,ElType.shiftable, 8, 22))

    myNeighborhood.houses.append(myHouse)

    test_list = myNeighborhood.testUseElAppliancesSoloNon("Oppgave1")
    for x in range(len(test_list)):
        print("powerload hour ",x+1," : ",test_list[x])

    #testHouseRandom = Household("random")
    #testHouseRandom.makeElappliances(5)

    #myNeighborhood.houses.append(testHouseRandom)

    myNeighborhood.updateTimetable("RTP")
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
