import optimization_task1 as opt
from objects import ElAppliance, Household, ElType

house = Household("Mi Casa", opt.appliances2)

hourly_prices = [0.1, 0.1, 0.3, 0.2, 0.1, 0.1, 0.2, 0.1, 0.3,
        0.3, 0.3, 0.2,0.3, 0.3, 0.3, 0.2,0.3, 0.3, 0.3, 0.2,0.3, 0.3, 0.3, 0.1]

df = opt.get_load_schedule(house.elAppliance, hourly_prices, task4=True, peak_load=3.7)

print(df)
