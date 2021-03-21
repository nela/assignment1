import copy
import enum
import random


# creating enumerations using class
class ElType(enum.Enum):
    shiftable = 1
    shiftable_non_continuous = 2
    non_shiftable_non_continuous = 3
    non_shiftable = 4


class ElAppliance:
    #type : 1 = shiftable, 2 = non-shiftable non-continious, 3 = non-shiftable
    def __init__(self, name, dailyUsageMin, dailyUsageMax, maxHourConsumption,
            duration, elType, timeMin = 0, timeMax = 24):
        self.name = name
        self.dailyUsageMin = dailyUsageMin
        self.dailyUsageMax = dailyUsageMax
        self.duration = duration
        self.timeMin = timeMin
        self.timeMax = timeMax
        self.maxHourConsumption = maxHourConsumption
        self.elType = elType


class Household:
    def __init__(self, name):
        self.name = name
        self.elAppliance = self.make_standard_appliances() + self.make_aux_appliancesFast()

    def make_standard_appliances(self):
        appliances = []
        appliances.append(ElAppliance("Lighting", 1, 2, 0.2, 10, ElType.non_shiftable, timeMin=10, timeMax=20))
        appliances.append(ElAppliance("Heating", 6.4, 9.6, 0.4, 24, ElType.non_shiftable, timeMin=0, timeMax=24))
        appliances.append(ElAppliance("Stove", 3.9, 3.9, 2, 3, ElType.shiftable, timeMin=14, timeMax=22))
        appliances.append(ElAppliance("Refrigerator", 1.32, 3.9, 0.164, 24, ElType.non_shiftable, timeMin=0, timeMax=24))
        appliances.append(ElAppliance("TV", 0.15, 0.6, 0.12, 5, ElType.non_shiftable, timeMin=17, timeMax=22))
        appliances.append(ElAppliance("Computer", 0.6, 0.6, 0.1, 6, ElType.non_shiftable, timeMin=8, timeMax=24))
        appliances.append(ElAppliance("Dishwasher", 1.44, 1.44, 1.44, 1, ElType.shiftable_non_continuous, timeMin=14, timeMax=24))
        appliances.append(ElAppliance("Laundry Machine", 1.94, 1.94, 0.485, 4, ElType.shiftable, timeMin=0, timeMax=18))
        appliances.append(ElAppliance("Cloth Dryer", 2.5, 2.5, 2.5, 1, ElType.shiftable, timeMin=0, timeMax=20))
        #.... Resten av standarde appliances

        # Deeop copy for å unngå statisk dritt
        return copy.deepcopy(appliances)

    def make_aux_appliancesFast(self):
        appliances = []

        appliances.append(ElAppliance("EV", 9.9, 9.9, 3.3, 3, ElType.shiftable_non_continuous, timeMin=0, timeMax=8))
        appliances.append(ElAppliance("Ceiling Fan", 0.22, 0.21, 0.073, 3, ElType.shiftable_non_continuous, timeMin=12, timeMax=20))
        appliances.append(ElAppliance("Refrigerator", 1.32, 3.9, 0.164, 24, ElType.non_shiftable, timeMin=0, timeMax=24))
        appliances.append(ElAppliance("Laundry Machine", 1.94, 1.94, 0.485, 4, ElType.shiftable, timeMin=0, timeMax=18))
        appliances.append(ElAppliance("Router", 0.14, 0.14, 0.006, 24, ElType.non_shiftable, timeMin=0,timeMax=24))
        # .... Resten av aux appliances

        # random.sample velger ut random appliances med antall=num_appliances
        return copy.deepcopy(appliances)

    def make_aux_appliances(self):
        appliances = []

        appliances.append(ElAppliance("EV", 9.9, 9.9, 3.3, 3, ElType.shiftable_non_continuous, timeMin=0, timeMax=8))
        appliances.append(ElAppliance("Ceiling Fan", 0.22, 0.21, 0.073, 3, ElType.shiftable_non_continuous, timeMin=12, timeMax=20))
        appliances.append(ElAppliance("Freezer", 0.84, 0.84,  0.035, 24, ElType.non_shiftable, timeMin=0, timeMax=24))
        appliances.append(ElAppliance("Cloth Iron", 0.28, 0.28, 0.28, 1, ElType.shiftable, timeMin=10, timeMax=20))
        appliances.append(ElAppliance("Router", 0.14, 0.14, 0.006, 24, ElType.non_shiftable, timeMin=0,timeMax=24))
        appliances.append(ElAppliance("Cellphone charger", 0.01, 0.01, 0.003, 4, ElType.shiftable_non_continuous, timeMin=0, timeMax=12))
        appliances.append(ElAppliance("Microwave", 0.6, 0.6, 0.6, 1, ElType.shiftable, timeMin=17, timeMax=24))
        appliances.append(ElAppliance("Hair Dryer", 0.19, 0.19, 0.19, 1, ElType.shiftable, timeMin=19, timeMax=23))
        appliances.append(ElAppliance("Toaster", 0.3, 0.3, 0.3, 1, ElType.shiftable, timeMin=12, timeMax=20))
        # .... Resten av aux appliances

        # Velg antall random appliances mellom 2 og antall appliances i lista
        num_appliances = random.randint(2, len(appliances)-1)

        # random.sample velger ut random appliances med antall=num_appliances
        return copy.deepcopy(random.sample(appliances, num_appliances))


class Neighbourhood:
    def __init__(self, name, num_houses):
        self.name = name
        self.num_houses = num_houses

        self.houses = []

        for i in range(num_houses):
            self.houses.append(Household("House_" + str(i)))
