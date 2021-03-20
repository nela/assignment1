from classes import ElType, ElAppliance, Household, Neighbourhood
import optimization_task1 as opt
from generate_rt_prices import daily_price

house = Household("Test House")

neighbourhood = Neighbourhood("Majorstua", 3)

hourly_prices = [0.2232432246591243,
        0.21439749417395604,
        0.22646127290367132,
        0.2019058902183628,
        0.2084472736282907,
        0.217188222977618,
        0.4834991686820009,
        0.6614948649077409,
        0.7969147784703379,
        0.7889633962332405,
        0.7784351162092065,
        0.6715152581213365,
        0.6598643685558833,
        0.5418542497470702,
        0.2330862791045794,
        0.21737128775227166,
        0.27858552538272263,
        0.31757909999476114,
        0.7331633241955074,
        0.6566771124454189,
        0.6342015945540525,
        0.5269793292089976,
        0.4775919568309417,
        0.44726107193671527]


house_schedule = opt.get_house_load_schedule(house, hourly_prices, peak_load)
print(house_schedule)

# neighbourhood_schedule = opt.get_neighbourhood_load_schedule(neighbourhood.houses, hourly_prices)
# print(neighbourhood_schedule)


load = opt.get_total_daily_load(house)
print(load)
